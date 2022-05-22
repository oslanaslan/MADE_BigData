#!/usr/bin/env python3
'''
Reducer for MapReduce
Removes prefix and creates groups of inputs
'''
import sys
import re

import random


n = random.randint(1, 5)
groups_lst = []
current_group_lst = []
i = 0

for line in sys.stdin:
    if i == n:
        i = 0
        groups_lst.append(','.join(current_group_lst))
        current_group_lst = []
        n = random.randint(1, 5)

    line = line.split('_')[1]
    line = re.sub(r"\s+", "", line)
    current_group_lst.append(line)
    i += 1

groups_lst.append(','.join(current_group_lst))
print('\n'.join(groups_lst), end='')
