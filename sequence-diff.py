#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import utils
from difflib import ndiff

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=True, nargs='+',
                        help='input files of sequences to be compared (the first file is the base to be compared with, \
                              such as reference translations)')
    parser.add_argument('-c', '--const', required=False, nargs='+', default=[],
                        help='files of sequences not participating in the comparison, \
                              such as source sentences to be translated')
    parser.add_argument('-ft', '--file-tag', required=False, nargs='+', help='tags of input files')
    parser.add_argument('-ct', '--const-tag', required=False, nargs='+', help='tags of const files')
    parser.add_argument('-d', '--condense', required=False, action="store_true",
                        help='condense the comparison of multiple sequences without showing diffs')
    parser.add_argument('-v', '--verbose', required=False, action="store_true",
                        help='print all sequences in the condense mode')
    args = parser.parse_args()

    if len(args.file) < 2:
        utils.error("At least two files should be provided for comparison.")
    tags = []
    if args.const_tag is not None:
        if len(args.const) != len(args.const_tag):
            utils.error("The number of const files and tags should be the same.")
        else:
            tags = args.const_tag
    else:
        for i in range(len(args.const)):
            tags.append("CONST-%d" % (i+1))
    if args.file_tag is not None:
        if len(args.file) != len(args.file_tag):
            utils.error("The number of input files and tags should be the same.")
        else:
            tags += args.file_tag
    else:
        tags.append("SEQUE-B")
        for i in range(1, len(args.file)):
            tags.append("SEQUE-%d" % (i+1))

    files = [open(f) for f in args.const+args.file]
    ref_index = len(args.const)
    for counter, lines in enumerate(zip(*files), start=1):
        seq_set = set()
        for i in range(ref_index, len(files)):
            seq_set.add(lines[i])
        if len(seq_set) > 1 or args.verbose:
            for i in range(ref_index):
                print("%d %s\t%s" % (counter, tags[i], lines[i].strip()))
            print("."*100)
        if args.verbose or len(seq_set) > 1 and args.condense:
            print("%d %s\t%s" % (counter, tags[ref_index], lines[ref_index].strip()))
        found_first_diff = False
        for i in range(ref_index+1, len(files)):
            has_diff = lines[ref_index] != lines[i]
            if args.verbose or has_diff and args.condense:
                print("%d %s\t%s" % (counter, tags[i], lines[i].strip()))
            if has_diff and not args.verbose and not args.condense:
                if found_first_diff:
                    print("."*100)
                for dl in ndiff([lines[ref_index]], [lines[i]]):
                    if dl[0] == '-':
                        print("%d %s\t%s" % (counter, tags[ref_index], dl.strip()[2:]))
                    elif dl[0] == '+':
                        print("%d %s\t%s" % (counter, tags[i], dl.strip()[2:]))
                    else:
                        print("           \t%s" % (dl.strip()[2:]))
                found_first_diff = True
        if len(seq_set) > 1 or args.verbose:
            print("="*100)
