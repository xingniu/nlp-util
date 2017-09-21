#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import tarfile
import re

def extract_text(filein):
    return filein.read().decode("utf-16").encode("utf-8").replace("\r","")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=True, help='input repacked tgz file')
    parser.add_argument('-s', '--source', required=True, help='source language (e.g. fr)')
    parser.add_argument('-t', '--target', required=False, help='target language (e.g. en)')
    parser.add_argument('-c', '--category', required=False, default="dev", help='dev or test?')
    parser.add_argument('-o', '--output', required=False, help='output file (used for parallel data)')
    args = parser.parse_args()

    parallel_data = {}
    
    source_pattern = "(.*/mslt_"+args.category+"_"+args.source+"_\d+/.+?).t2..*"
    with tarfile.open(args.file, "r:gz") as tar:
        for tarinfo in tar.getmembers():
            match = re.match(source_pattern, tarinfo.name.lower())
            if match != None:
                text = extract_text(tar.extractfile(tarinfo))
                parallel_data[match.group(1)] = {"src":text}
                
    if args.target:
        target_pattern = "(.*/mslt_"+args.category+"_"+args.source+"_\d+/.+?).t[3-9]."+args.target+".*"
        with tarfile.open(args.file, "r:gz") as tar:
            for tarinfo in tar.getmembers():
                match = re.match(target_pattern, tarinfo.name.lower())
                if match != None:
                    text = extract_text(tar.extractfile(tarinfo))
                    parallel_data[match.group(1)]["tgt"] = text
        
        output_src = open(args.output+"."+args.source, "wb")
        output_tgt = open(args.output+"."+args.target, "wb")
        for item in parallel_data.iteritems():
            assert len(item[1]) == 2
            if item[1]["src"].strip() != "" and item[1]["tgt"].strip() != "":
                output_src.write(item[1]["src"])
                output_tgt.write(item[1]["tgt"])
        output_src.close()
        output_tgt.close()
    else:
        for value in parallel_data.itervalues():
            print value["src"].strip()