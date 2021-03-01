#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open("weather.py") as fp:
    for i, line in enumerate(fp):
        if "\xe2" in line:
            print (i, repr(line))
