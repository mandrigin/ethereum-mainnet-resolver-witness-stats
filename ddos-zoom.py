import pandas as pd
import matplotlib.pyplot as plt
import numpy


import sys
import csv


def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x.values, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)


try:
    filename = str(sys.argv[1])
    fromblock = 2400000
    toblock = 2730000
except:
    print "usage: python ddos_zoom.py <filename>"
    exit(1)


series = {}
with open(filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1
        if int(row['blockNum']) < fromblock:
            continue

        if int(row['blockNum']) > toblock:
            break

        for k, v in row.iteritems():
            series[k.upper()] = series.get(k.upper(), [])
            series[k.upper()].append(int(v))

        if line_count % 100000 == 0:
            print "processed", line_count, "rows"

df = pd.DataFrame(series)
print df

plt.ylabel("MB")
plt.xlabel("block #")
plt.grid(True)


plt.plot(
    df['BLOCKNUM'],
    df['WITNESSESSIZE']/1024.0/1024.0,
    label="Witnesses")


plt.show()

