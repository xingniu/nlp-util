#!/usr/bin/env python -*- coding: utf-8 -*-

import numpy as np
import argparse
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, help='input file(s) (glob patterns are supported)')
    parser.add_argument('-c', '--column', required=False, type=int, default=0, help='the index of column that contains values')
    parser.add_argument('-n', '--normalize', required=False, action="store_true", help='normalize scores to [-1,1]')
    parser.add_argument('-l', '--lower', required=False, type=float, help='the lower range of bins')
    parser.add_argument('-u', '--upper', required=False, type=float, help='the upper range of bins')
    parser.add_argument('-b', '--bins', required=False, type=int, default=10, help='the number of bins')
    parser.add_argument('-p', '--plot', required=False, action="store_true", help='plot the histogram')
    args = parser.parse_args()

    scores = []
    for line in utils.get_input(args.input):
        score = utils.str2float(line.split()[args.column])
        if score != None:
            scores.append(score)
    lower = np.min(scores)
    upper = np.max(scores)
    magnitude = np.max(np.abs(scores))
    norm_lower = -1
    norm_upper = 1

    if args.lower is not None and args.upper is not None:
        if args.normalize:
            lower = args.lower * magnitude
            upper = args.upper * magnitude
            norm_lower = args.lower
            norm_upper = args.upper
        else:
            lower = args.lower
            upper = args.upper

    if args.normalize:
        bin_edges = np.linspace(norm_lower, norm_upper, args.bins+1, endpoint=True)
    else:
        bin_edges = np.linspace(lower, upper, args.bins+1, endpoint=True)

    interval = (upper-lower)*1.0/args.bins
    if interval >= 2:
        decimal = str(0)
    elif interval >= 0.1:
        decimal = str(1)
    else:
        decimal = str(2)
    df = "%."+decimal+"f"

    bin_labels = [("["+df+","+df+")") % (bin_edges[i], bin_edges[i+1]) for i in range(len(bin_edges)-1)]
    bin_labels[-1] = bin_labels[-1][:-1]+"]"

    hist = np.histogram(scores, bins=args.bins, range=(lower,upper))
    for i in range(len(hist[0])):
        print((df+"\t%s\t%.6f") % (bin_edges[i], bin_labels[i], float(hist[0][i])/len(scores)))
    print(df % bin_edges[-1])

    if args.plot:
        import matplotlib.pyplot as plt
        width = (bin_edges[1]-bin_edges[0])/2.0
        plt.xticks(bin_edges[:-1], bin_labels)
        plt.bar(bin_edges[:-1], hist[0]/float(len(scores)), width, align='center', alpha=0.5)
        plt.xlim([2*bin_edges[0]-bin_edges[1], bin_edges[-1]])
        plt.show()
