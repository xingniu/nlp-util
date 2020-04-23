#!/usr/bin/env python -*- coding: utf-8 -*-

import re
import argparse
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=True, help='XLIFF file')
    parser.add_argument('-s', '--side', required=False, default="both", choices=["source", "target", "both", "reverse"],
                        help='side(s) of the bitext to be extracted')
    args = parser.parse_args()

    tree = ET.parse(args.file)
    root = tree.getroot()
    namespace = re.match(r'\{.+\}', root.tag)[0]
    for segment in root.iter('%ssegment' % namespace):
        source = segment.find('%ssource' % namespace).text
        target = segment.find('%starget' % namespace).text
        if args.side == "source":
            print(source)
        elif args.side == "target":
            print(target)
        elif args.side == "both":
            print("%s\t%s" % (source, target))
        elif args.side == "reverse":
            print("%s\t%s" % (target, source))
