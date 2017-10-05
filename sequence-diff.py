#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import utils
from itertools import izip
from difflib import ndiff

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=True, nargs='+', \
        help='input files of sequences to be compared (the first file is the base to be compared with, \
        such as reference translations)')
    parser.add_argument('-c', '--const', required=False, nargs='+', default=[], \
        help='files of sequences not participating in comparison, such as source sentences to be translated')
    args = parser.parse_args()
    
    if len(args.file) < 2:
        utils.error("At least two files should be provided for comparison.")
    
    files = [open(f) for f in args.const+args.file]
    ref_index = len(args.const)
    counter = 0
    for lines in izip(*files):
        seq_set = set()
        for i in xrange(ref_index, len(files)):
            seq_set.add(lines[i])
        if len(seq_set) > 1:
            for i in xrange(ref_index):
                print "%d CONST-%d\t%s" % (counter, i, lines[i].strip())
            for i in xrange(ref_index+1,len(files)):
                if lines[ref_index] != lines[i]:
                    print "."*100
                    for dl in ndiff([lines[ref_index]], [lines[i]]):
                        if dl[0] == '-':
                            print "%d SEQUE-%d\t%s" % (counter, 0, dl.strip()[2:])
                        elif dl[0] == '+':
                            print "%d SEQUE-%d\t%s" % (counter, i-ref_index, dl.strip()[2:])
                        else:
                            print "           \t%s" % (dl.strip()[2:])
            print "="*100
        counter += 1