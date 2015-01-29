import csv

csv_in = open('mycsv.csv','rb')
myreader = csv.reader(csv_in)

bus_id, bus_name, voltage = zip(*myreader)
voltage = map(float, voltage)