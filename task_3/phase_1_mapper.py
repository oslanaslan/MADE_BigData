#!/usr/bin/env python3
'''
Stackoverflow most common tag counter
Phase 1 mapper

'''
import re
import sys


TARGET_YEARS = ['2010', '2016']
tag_pattern = re.compile(r'Tags="[^"]*')
year_pattern = re.compile(r'CreationDate="[^"]*')
left_tag_pattern = re.compile(r'&lt')
right_tag_pattern = re.compile(r'&gt')

for line in sys.stdin:
    year_search = year_pattern.search(line)
    tag_search = tag_pattern.search(line)

    if year_search and tag_search:
        year = year_search.group()
        year = year.split('=')[1].strip('"').split('-')[0]

        if year in TARGET_YEARS:
            result_lst = tag_search.group()
            result_lst = left_tag_pattern.sub('', result_lst)
            result_lst = right_tag_pattern.sub('', result_lst)
            result_lst = result_lst.split('=')[1].strip('"').split(';')
            result_lst = [itm for itm in result_lst if itm]

            for res in result_lst:
                print(year, res, 1, sep='\t')
