#!/usr/bin/env python -*- coding: utf-8 -*-

import re
import argparse
import tarfile
from HTMLParser import HTMLParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def extract_xml(filein, langs, elements):
    working_element = None
    valid_lang = True
    texts = []
    guid = None
    for line in filein:
        line = line.strip()
        if line:
            if line.startswith("<dc:lang>"):
                lang = re.match("<dc:lang>(\w+)</dc:lang>", line).groups()[0]
                if langs and lang not in langs:
                    valid_lang = False
            elif line == "</item>":
                if valid_lang:
                    assert guid != None
                    yield guid,texts
                valid_lang = True
                texts = []
                guid = None
            elif line.startswith("<post:resource_guid>"):
                guid = re.match("<post:resource_guid>(.+)</post:resource_guid>", line).groups()[0]
            else:
                if not working_element:
                    for element in elements:
                        start_tag = "<"+element+">"
                        if line.startswith(start_tag):
                            line = line.replace(start_tag,"")
                            working_element = "</"+element+">"
                            break
                if working_element:
                    if line.endswith(working_element):
                        line = line.replace(working_element,"")
                        working_element = None
                    line = line.strip()
                    if line:
                        texts.append(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=True, nargs='+', help='Spinn3r tar.gz file(s)')
    parser.add_argument('-l', '--languages', required=False, nargs='+', help='language(s) to be extracted (e.g. en)')
    parser.add_argument('-e', '--elements', required=True, nargs='+', help='element(s) to be extracted (e.g. title, description)')
    parser.add_argument('-u', '--unescape', required=False, action="store_true", help='unescape text (e.g. "&amp;"->"&")')
    parser.add_argument('-c', '--clean', required=False, action="store_true", help='clean text (drop <*>/URLs, condense spaces)')
    args = parser.parse_args()
    
    langs = set(args.languages)
    elements = set(args.elements)
    hp = HTMLParser()
    
    for file_path in args.file:
        with tarfile.open(file_path, "r:gz") as tar:
            for tarinfo in tar.getmembers():
                if tarinfo.name.endswith(".xml"):
                    for guid,texts in extract_xml(tar.extractfile(tarinfo), langs, elements):
                        print "---%s---\n" % guid
                        for text in texts:
                            if args.unescape or args.clean:
                                text = hp.unescape(text.decode('utf-8'))
                                if "&" in text:
                                    text = hp.unescape(text)
                                if args.clean:
                                    text += " "
                                    text = re.sub("<[^<>]*>", " ", text) # drop anything in <>
                                    text = re.sub("\w+://[^ ]+ ", " ", text) # drop URLs
                                    text = re.sub("\s+"," ",text).strip() # condense spaces
                                    if not text:
                                        continue
                            print text.encode('utf-8')
                        print ""