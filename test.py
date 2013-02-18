#!/usr/bin/python

# menu2.py

import DFfilters

class Main():
    data = [1,2,3,4,5,6,7,8,9,10]
    n = 3
    fil = DFfilters.filters()
    print fil.Simple_Moving_Average(data, n)