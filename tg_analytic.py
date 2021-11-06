#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

seta = set()


# write data to csv
def statistics(user_id):
    with open('data.csv', 'a', newline="") as fil:


        if not str(user_id) in seta:
            fil.writelines('\n'+str(user_id)+'\n')
        seta.add(str(user_id))
