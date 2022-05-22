#!/usr/bin/env python3
'''
Stackoverflow most common tag counter
Phase 2 mapper

'''
import sys


for line in sys.stdin:
    year, tag, count = line.strip('\n').split('\t')
    print(year, tag, count, count, sep='\t')
