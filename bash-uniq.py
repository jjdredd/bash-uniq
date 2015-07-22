#!/usr/bin/env python3


####################################################################
# Filter out quotes that have already been read at bash.im/abyss   #
# and print new ones on stdout. Quote db in ./history (must exist) #
# Author: jjdredd                                                  #
####################################################################


import requests
import aggregator

abyss = 'http://bash.im/abyss'

lines = [line.strip(' \n') for line in open('history')]
a = aggregator.Aggregator(lines)
N = n = len(lines)

while True:
    # no need to update url, that page always gives new quotes
    page = requests.get(abyss)
    a.feed(page.text)
    l = len(a.read)
    if n == l:
        break
    else:
        n = l

if N == n:
    print('No new quotes.')
else:
    print(a.text)
    fout = open('history', 'w')
    for x in a.read:
        fout.write('{}\n'.format(x))
