#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from anaouder.text import normalize_sentence
from anaouder.version import VERSION



def main_normalizan(*args, **kwargs):
    """ normalizan cli entry point """
    
    parser = argparse.ArgumentParser(
        prog = "normalizan",
        description = "Normalize a text file")
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="write to a file")
    parser.add_argument("-r", "--reformat", action="store_true",
        help="reformat text file using punctuation, to put one sentence per line")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()
    
    input = open(args.input, 'r') if args.input else sys.stdin
    output = open(args.output, 'w') if args.output else sys.stdout

    while True:
        data = input.readline()
        if data:
            print(normalize_sentence(data), file=output)
        else:
            break
    
    if args.input:
        input.close()
    if args.output:
        output.close()


if __name__ == "__main__":
    main_normalizan()
