#!/usr/bin/env python3
'''
Stackoverflow most common tag counter
Phase 2 reducer

'''
import sys


TOP_N = 10
WORK_YEARS = [2010, 2016]
top_lists = {year: list() for year in WORK_YEARS}

for line in sys.stdin:
    (year, tag, counts, _) = line.strip('\n').split("\t")
    counts = int(counts)
    year = int(year)

    if year in WORK_YEARS:
        if len(top_lists[year]) < TOP_N:
            top_lists[year].append((year, tag, counts))
            top_lists[year] = sorted(
                    top_lists[year],
                    key=(lambda x: x[2]),
                    reverse=True,
            )
        else:
            if top_lists[year][-1][2] < counts:
                top_lists[year].append((year, tag, counts))
                top_lists[year] = sorted(
                    top_lists[year],
                    key=(lambda x: x[2]),
                    reverse=True,
                )
                top_lists[year] = top_lists[year][:TOP_N]
    else:
        raise ValueError(f"Got unexpected year: {year}")

for top_n_lst in top_lists.values():
    for (year, tag, counts) in top_n_lst:
        print(year, tag, counts, sep='\t')
