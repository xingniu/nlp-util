#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import utils
from collections import Counter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, help='input file(s) (glob patterns are supported)')
    parser.add_argument('-w', '--white-list', required=False, help='only count words in the write list')
    parser.add_argument('-b', '--black-list', required=False, help='ignore words in the black list')
    parser.add_argument('-s', '--statistics', required=False, action="store_true", help='print statistics')
    args = parser.parse_args()

    if args.white_list:
        white_list = set(word for line in utils.get_input(args.white_list) for word in line.split())
    elif args.black_list:
        black_list = set(word for line in utils.get_input(args.black_list) for word in line.split())

    counter = Counter()
    for line in utils.get_input(args.input):
        if args.white_list:
            counter.update(word for word in line.split() if word in white_list)
        elif args.black_list:
            counter.update(word for word in line.split() if word not in black_list)
        else:
            counter.update(line.split())

    total = 0
    for item in counter.most_common():
        print("%s\t%d" % (item[0].encode('utf8'), item[1]))
        total += item[1]
    if args.statistics:
        print("### |WORD|\t%d" % total)
        print("### |TYPE|\t%d" % len(counter))