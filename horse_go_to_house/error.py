import csv
from pandas.core.common import flatten

MANUAL = []
TIMING = []

csv_file = open("manual.csv", "r", encoding="Shift_jis")
MANUAL_READER = csv.reader(csv_file, delimiter="\n")
for manual in MANUAL_READER:
	MANUAL.append(manual) 

MANUAL = list(flatten(MANUAL))

csv_file = open("a.csv", "r", encoding="Shift_jis")
TIMING_READER = csv.reader(csv_file, skipinitialspace=True)
for timing in TIMING_READER:
	TIMING.append(timing)

TIMING = list(flatten(TIMING))

for i in range(len(TIMING)):
	if abs(float(TIMING[i])-float(MANUAL[i])) < 0.1:
		print(0)
	else: print(float(TIMING[i])-float(MANUAL[i]))