#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import utils
import re
import numpy as np

def decimals(value_str):
    integer_decimal = value_str.split(".")
    if len(integer_decimal) == 1:
        return 0
    else:
        return len(integer_decimal[1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, help='input file(s) (glob patterns are supported)')
    parser.add_argument('-m', '--metrics', required=False, nargs='+', default=["mean"], 
                        choices=["mean", "min", "max", "range", "median", "sum", "std", "var", "sub"],
                        help='statistic metrics')
    parser.add_argument('-l', '--label', required=False, action="store_true", help='print metrics labels')
    parser.add_argument('-c', '--column', required=False, type=int, help='analyze a specified swhitespace-split column (c-th)')
    args = parser.parse_args()
    placeholder="#PH#"

    value_str_mat = []
    for line in utils.get_input(args.input):
        if args.column != None:
            line = line.split()[args.column-1]
        value_strs = re.findall("-?\d+\.*\d*(?:e[+-]\d+)?", line)
        if len(value_str_mat) != 0 and len(value_strs) != len(value_str_mat[0]):
            continue
        value_str_mat.append(value_strs)
        template = line.rstrip()
    if len(value_str_mat) != 0:
        for value_str in value_str_mat[-1]:
            template = re.sub(value_str, placeholder, template, count=1)

    value_mat = [[float(value_str) for value_str in value_str_list] for value_str_list in value_str_mat]
    decimals_mat = [[decimals(value_str) for value_str in value_str_list] for value_str_list in value_str_mat]
    decimals_str_list = [str(dec) for dec in np.amax(decimals_mat, 0)]

    for metrics in args.metrics:
        if metrics == "mean":
            result_list = np.mean(value_mat, 0)
        elif metrics == "min":
            result_list = np.amin(value_mat, 0)
        elif metrics == "max":
            result_list = np.amax(value_mat, 0)
        elif metrics == "range":
            result_list = np.ptp(value_mat, 0)
        elif metrics == "median":
            result_list = np.median(value_mat, 0)
        elif metrics == "sum":
            result_list = np.sum(value_mat, 0)
        elif metrics == "std":
            result_list = np.std(value_mat, 0)
        elif metrics == "var":
            result_list = np.var(value_mat, 0)
        elif metrics == "sub":
            result_list = np.subtract(value_mat[0], value_mat[1])
        output_str = template
        for i in range(len(decimals_str_list)):
            print_format = "%."+decimals_str_list[i]+"f"
            output_str = re.sub(placeholder, print_format % result_list[i], output_str, count=1)
        if args.label:
            print("%s\t%s" % (metrics, output_str))
        else:
            print(output_str)
