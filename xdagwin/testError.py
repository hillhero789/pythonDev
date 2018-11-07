#!/usr/bin/python
# # -*- coding: utf-8 -*-

s = 0
for a in 'a2d3mckd4llfdsa00/fda3f+f2':
    if a.isdigit():
        s += int(a)
print(s)