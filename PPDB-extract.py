#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import re
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=False, help='input file (unzipped, glob patterns are supported)')
    parser.add_argument('-a', '--feature', required=False, help='the feature used for filtering')
    parser.add_argument('-t', '--threshold', required=False, type=float, help='the threshold used for filtering (keep >=)')
    parser.add_argument('-e', '--entailment', required=False, help='the entailment type used for filtering (RE)')
    args = parser.parse_args()
    
    for line in utils.get_input(args.file):
        additional_info = ""
        segs = line.strip().split(" ||| ")
        if args.feature:
            for feature in segs[3].split():
                match = re.match(args.feature+"=(.+)",feature)
                if match:
                    score = float(match.group(1))
                    break
            if match:
                additional_info += "\t"+match.group(1)
                if args.threshold and score < args.threshold:
                    continue
            else:
                continue
        if args.entailment:
            match = re.match(args.entailment,segs[5])
            if match:
                additional_info += "\t"+match.group(0)
            else:
                continue
        print "%s\t%s%s" % (segs[1].encode('utf8'),segs[2].encode('utf8'),additional_info)