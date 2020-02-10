import pandas as pd
import matplotlib.pyplot as plt

import sys
import csv

try:
    filename = str(sys.argv[1])
    fromblock = 0
    if len(sys.argv) == 3:
        fromblock = int(sys.argv[2])
except:
    print "usage: python quantile-analysis.py <filename> [<fromblock>]"
    exit(1)

series = {}
with open(filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1

        if int(row['blockNum']) < fromblock:
            continue
        for k, v in row.iteritems():
            series[k] = series.get(k, [])
            series[k].append(int(v))

        if line_count % 100000 == 0:
            print "processed hex", line_count, "rows"

df = pd.DataFrame(series)
print df

print 'quantile analysis'
print "mean", df['witnessesSize'].mean()/1024.0/1024.0
print "median", df['witnessesSize'].median()/1024.0/1024.0
print "percentile 90th", df['witnessesSize'].quantile(0.9)/1024.0/1024.0
print "percentile 95th", df['witnessesSize'].quantile(0.95)/1024.0/1024.0
print "percentile 99th", df['witnessesSize'].quantile(0.99)/1024.0/1024.0
print "percentile 100th", df['witnessesSize'].quantile(1.0)/1024.0/1024.0

plt.xlabel("MB")

plt.boxplot(df['witnessesSize']/1024.0/1024.0, vert=False, labels=["witnessesSize"], showfliers=False, whis=[1,99])

plt.show()
