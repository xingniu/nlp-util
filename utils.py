#!/usr/bin/env python -*- coding: utf-8 -*-

import fileinput
import glob
import sys
import numpy as np

def error(message):
    print >> sys.stderr, message
    sys.exit()

def warning(message):
    print >> sys.stderr, message

def get_input(file_pattern, encoding="utf8"):
    file_list = []
    if file_pattern:
        file_list = glob.glob(file_pattern)
        if len(file_list) == 0:
            error("No input files found.")
    return fileinput.input(file_list, openhook=fileinput.hook_encoded(encoding))

def str2float(string):
    try:
        value = float(string)
        if np.isnan(value):
            warning("ignored value: NaN")
            return None
        else:
            return value
    except ValueError:
        warning("ignored invalid literal: %s" % string)
        return None
