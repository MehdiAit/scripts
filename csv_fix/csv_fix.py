import csv

csv_row = []
to_write = []

with open('igs.csv','r') as my_file:
    csv_row = [l for l in csv.reader(my_file)]

for x in csv_row:
    if len(x[0].split(" ")) >= 2:
        x[0] = "_".join(x[0].split(" "))
    to_write.append(x)

with open("igs_filtred.csv","w") as new:
    wr = csv.writer(new)
    wr.writerows(to_write)
