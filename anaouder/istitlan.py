#!/usr/bin/env python3

import sys
from anaouder import main_adskrivan


def main_istitlan(*args):
	args = args[1:] + ("-t", "srt")
	main_adskrivan(*args)


if __name__ == "__main__":
	main_istitlan(*sys.argv)