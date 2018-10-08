#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
from difflib import SequenceMatcher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=True, nargs=2, help='input bitext files to be compared')
    parser.add_argument('-o', '--output', required=False, nargs=2, help='output bitext files without identical pairs')
    parser.add_argument('-t', '--threshold', required=False, type=float, default=0.9,
                        help='similarity threshold to determine identity ([0,1])')
    parser.add_argument('-l', '--lowercase', required=False, action="store_true", help='compare lowercased sequences')
    parser.add_argument('-v', '--verbose', required=False, action="store_true", help='print identical pairs')
    args = parser.parse_args()

    if args.output:
        output0 = open(args.output[0], 'w')
        output1 = open(args.output[1], 'w')

    files = [open(f) for f in args.file]
    counter = 0
    identical = 0
    for lines in zip(*files):
        counter += 1
        str0 = lines[0].lower().strip() if args.lowercase else lines[0].strip()
        str1 = lines[1].lower().strip() if args.lowercase else lines[1].strip()
        ratio = SequenceMatcher(None, str0, str1).ratio()
        if ratio >= args.threshold:
            identical += 1
            if args.verbose:
                print("%d\tsimilarity=%.2f" % (counter, ratio))
                print("FILE-1\t%s" % lines[0].strip())
                print("FILE-2\t%s" % lines[1].strip())
                print("="*100)
        elif args.output:
            output0.write(lines[0].strip()+"\n")
            output1.write(lines[1].strip()+"\n")
    percentile = identical*100.0/counter
    print("%d bitext pairs were read" % counter)
    print("%d pairs (%.2f%%) were identical with threshold=%.2f" % (identical, percentile, args.threshold))

    if args.output:
        output0.close()
        output1.close()
