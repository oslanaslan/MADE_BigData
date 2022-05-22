#!/usr/bin/env python3
'''
Mapper for MapReduce
Adds random prefix to input
'''
import sys
import re

import random


lines_lst = []

for line in sys.stdin:
    lines_lst.append(
        str(random.randint(1, 1e5)) + '_' + re.sub(r"\s+", "", line)
    )

print('\n'.join(lines_lst))
