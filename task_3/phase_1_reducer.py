#!/usr/bin/env python3
'''
Stackoverflow most common tag counter
Phase 1 reducer

'''
import sys


current_tag = None
current_year = None
current_ctr = 0

for line in sys.stdin:
    year, tag, counts = line.strip('\n').split("\t", 2)
    counts = int(counts)

    if current_tag:
        if current_tag == tag and current_year == year:
            current_ctr += counts
        else:
            print(current_year, current_tag, current_ctr, sep='\t')
            current_tag = tag
            current_year = year
            current_ctr = counts
    else:
        current_tag = tag
        current_year = year
        current_ctr = counts

if current_tag:
    print(current_year, current_tag, current_ctr, sep='\t')
