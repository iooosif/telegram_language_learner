#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

seta = set()


# write data to csv
def statistics(user_id):

    with open('data.csv', 'a', newline="") as fil:

        wr = csv.writer(fil, delimiter=';')
        wr.writerow([user_id])

