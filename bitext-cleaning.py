#!/usr/bin/env python -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import sys
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=False, nargs='+', help='input bitext file(s)')
    parser.add_argument('-o', '--output', required=False, nargs='+', help='output bitext file(s)')
    parser.add_argument('-r', '--ratio', required=False, type=float, default=None,
                        help='remove pairs which length ratios are no less than a threshold')
    parser.add_argument('-i', '--incomplete', required=False, action="store_true",
                        help='remove pairs if they contain incomplete sentences, i.e. no .!?" at the end')
    parser.add_argument('-u', '--uppercase', required=False, action="store_true",
                        help='remove pairs if both source and target are uppercased, otherwise capitalize uppercase strings')
    parser.add_argument('-v', '--verbose', required=False, action="store_true", help='print identified pairs')
    args = parser.parse_args()

    eos_punctuations = ".!?\""

    if args.output:
        output0 = open(args.output[0], 'w')
        if len(args.output) == 2:
            output1 = open(args.output[1], 'w')

    files = [open(f) for f in args.file] if args.file else [utils.get_input(args.file)]
    filtered_counter = imbalance = incomplete = uppercase = 0
    capitalized = 0
    for counter, lines in enumerate(zip(*files), start=1):
        filtered = False
        info = ""
        if len(files) == 1:
            lines = lines[0].split("\t")
        str0 = lines[0].strip()
        str1 = lines[1].strip()

        if args.ratio is not None:
            str0_tokens = str0.split()
            str1_tokens = str1.split()
            ratio01_token = 1.0*len(str0_tokens)/len(str1_tokens)
            ratio10_token = 1.0*len(str1_tokens)/len(str0_tokens)
            ratio01_char = 1.0*len(str0)/len(str1)
            ratio10_char = 1.0*len(str1)/len(str0)
            max_ratio = max(ratio01_token, ratio10_token, ratio01_char, ratio10_char)
            if max_ratio >= args.ratio:
                filtered = True
                info += "length-ratio=%.2f " % max_ratio
                imbalance += 1
        if args.incomplete:
            if len(str0) == 0 or len(str1) == 0 or str0[-1] not in eos_punctuations or str1[-1] not in eos_punctuations:
                filtered = True
                info += "incomplete=True "
                incomplete += 1
        if args.uppercase:
            str0_isupper = str0.isupper()
            str1_isupper = str1.isupper()
            if str0_isupper and not str1_isupper:
                str0 = str0.capitalize()
                capitalized += 1
            elif not str0_isupper and str1_isupper:
                str1 = str1.capitalize()
                capitalized += 1
            elif str0_isupper and str1_isupper:
                filtered = True
                info += "uppercase=True "
                uppercase += 1

        if filtered:
            filtered_counter += 1
            if args.verbose:
                print("%d\t%s" % (counter, info), file=sys.stderr)
                print("FILE-1\t%s" % str0, file=sys.stderr)
                print("FILE-2\t%s" % str1, file=sys.stderr)
                print("="*100, file=sys.stderr)
        else:
            if args.output:
                if len(args.output) == 2:
                    output0.write(str0+"\n")
                    output1.write(str1+"\n")
                else:
                    output0.write(str0+"\t"+str1+"\n")
            elif args.file is None:
                print(str0+"\t"+str1)
    percentile = filtered_counter*100.0/counter
    print("%d bitext pairs were read" % counter, file=sys.stderr)
    print("%d pairs (%.2f%%) were filtered out" % (filtered_counter, percentile), file=sys.stderr)
    if args.ratio is not None:
        percentile = imbalance*100.0/counter
        print("- %d pairs (%.2f%%) were imbalanced with length-ratio >= %.2f"
              % (imbalance, percentile, args.ratio), file=sys.stderr)
    if args.incomplete:
        percentile = incomplete*100.0/counter
        print("- %d pairs (%.2f%%) contain incomplete sentences." % (incomplete, percentile), file=sys.stderr)
    if args.uppercase:
        percentile = uppercase*100.0/counter
        print("- %d pairs (%.2f%%) were uppercased (both source and target)" % (uppercase, percentile), file=sys.stderr)
        percentile = capitalized*100.0/counter
        print("%d pairs (%.2f%%) have been capitalized" % (capitalized, percentile), file=sys.stderr)

    if args.output:
        output0.close()
        if len(args.output) == 2:
            output1.close()
