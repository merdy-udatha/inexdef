import argparse
import gzip
import sys

filename = sys.argv[1]
if filename.endswith('.gz'): fp = gzip.open(filename, 'rt')
else:                        fp = open(filename)

