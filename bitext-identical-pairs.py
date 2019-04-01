#!/usr/bin/env python -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import string
import sys
import re
import utils
from difflib import SequenceMatcher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=False, nargs='+', help='input bitext file(s) to be compared')
    parser.add_argument('-o', '--output', required=False, nargs='+', help='output bitext file(s) without identical pairs')
    parser.add_argument('-i', '--inclusion', required=False, action="store_true", help='treat inclusion as identity')
    parser.add_argument('-t', '--threshold', required=False, type=float, default=0.9,
                        help='similarity threshold to determine identity ([0,1])')
    parser.add_argument('-c', '--character', required=False, action="store_true", help='calculate character-level similarity')
    parser.add_argument('-p', '--punctuation', required=False, action="store_true", help='do not compare punctuations')
    parser.add_argument('-l', '--lowercase', required=False, action="store_true", help='compare lowercased sequences')
    parser.add_argument('-v', '--verbose', required=False, action="store_true", help='print identical pairs')
    args = parser.parse_args()

    python3 = utils.isPython3()
    if python3:
        punctuations = str.maketrans('', '', string.punctuation)
    whitespaces = re.compile(r"\s+")

    if args.output:
        output0 = open(args.output[0], 'w')
        if len(args.output) == 2:
            output1 = open(args.output[1], 'w')

    files = [open(f) for f in args.file] if args.file else [utils.get_input(args.file)]
    counter = 0
    identical = 0
    for lines in zip(*files):
        counter += 1
        if len(files) == 1:
            lines = lines[0].split("\t")
        str0 = lines[0].lower().strip() if args.lowercase else lines[0].strip()
        str1 = lines[1].lower().strip() if args.lowercase else lines[1].strip()
        if args.punctuation:
            if python3:
                str0 = str0.translate(punctuations)
                str1 = str1.translate(punctuations)
            else:
                str0 = str0.translate(None, string.punctuation)
                str1 = str1.translate(None, string.punctuation)
        inclusion = str0 in str1 or str1 in str0 if args.inclusion else False
        if not inclusion:
            if args.character:
                ratio = SequenceMatcher(None, whitespaces.sub("", str0), whitespaces.sub("", str1)).ratio()
            else:
                ratio = SequenceMatcher(None, str0.split(), str1.split()).ratio()
        if inclusion or ratio >= args.threshold:
            identical += 1
            if args.verbose:
                if inclusion:
                    print("%d\tinclusion=True" % counter, file=sys.stderr)
                else:
                    print("%d\tsimilarity=%.2f" % (counter, ratio), file=sys.stderr)
                print("FILE-1\t%s" % lines[0].strip(), file=sys.stderr)
                print("FILE-2\t%s" % lines[1].strip(), file=sys.stderr)
                print("="*100, file=sys.stderr)
        else:
            if args.output:
                if len(args.output) == 2:
                    output0.write(lines[0].strip()+"\n")
                    output1.write(lines[1].strip()+"\n")
                else:
                    output0.write(lines[0].strip()+"\t"+lines[1].strip()+"\n")
            elif args.file is None:
                print(lines[0].strip()+"\t"+lines[1].strip())
    percentile = identical*100.0/counter
    print("%d bitext pairs were read" % counter, file=sys.stderr)
    if args.inclusion:
        print("%d pairs (%.2f%%) were identical with inclusion and threshold=%.2f"
              % (identical, percentile, args.threshold), file=sys.stderr)
    else:
        print("%d pairs (%.2f%%) were identical with threshold=%.2f"
              % (identical, percentile, args.threshold), file=sys.stderr)

    if args.output:
        output0.close()
        if len(args.output) == 2:
            output1.close()
