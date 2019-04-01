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
                        help='filter out pairs which length ratios are no less than a threshold')
    parser.add_argument('-c', '--capitalize', required=False, action="store_true",
                        help='capitalize strings if all characters are uppercase')
    parser.add_argument('-v', '--verbose', required=False, action="store_true", help='print identified pairs')
    args = parser.parse_args()

    if args.output:
        output0 = open(args.output[0], 'w')
        if len(args.output) == 2:
            output1 = open(args.output[1], 'w')

    files = [open(f) for f in args.file] if args.file else [utils.get_input(args.file)]
    counter = 0
    filtered_counter = imbalance = capitalized = 0
    for lines in zip(*files):
        filtered = False
        info = ""
        counter += 1
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
        if args.capitalize:
            str0_isupper = str0.isupper()
            str1_isupper = str1.isupper()
            if str0_isupper and not str1_isupper:
                str0 = str0.capitalize()
                capitalized += 1
            if not str0_isupper and str1_isupper:
                str1 = str1.capitalize()
                capitalized += 1

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
        print("%d pairs (%.2f%%) were imbalanced with length-ratio >= %.2f"
              % (imbalance, percentile, args.ratio), file=sys.stderr)
    if args.capitalize:
        percentile = capitalized*100.0/counter
        print("%d pairs (%.2f%%) were capitalized" % (capitalized, percentile), file=sys.stderr)

    if args.output:
        output0.close()
        if len(args.output) == 2:
            output1.close()
