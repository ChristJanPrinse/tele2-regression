import csv

bus_numbers = ['101', '102', '36', '40']
bus_names = ['NUC_A', 'NUC_B', 'CATDOG', 'HYDRO_A']
voltage = [.99, 1.02, 1.01, 1.00]

# open a file for writing.
csv_out = open('mycsv.csv', 'wb')

# create the csv writer object.
mywriter = csv.writer(csv_out)

# all rows at once.
rows = zip(bus_numbers, bus_names, voltage)
mywriter.writerows(rows)

# always make sure that you close the file.
# otherwise you might find that it is empty.
csv_out.close()