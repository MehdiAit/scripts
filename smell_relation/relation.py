import os
import csv
import argparse

def readCsv(csvFiles):
    globalSet = []
    myList = []
    for csvfile in csvFiles:
        methlist = {}
        with open(csvfile,"r") as csvCS:
            methlist = {l[1] for l in csv.reader(csvCS)}
            globalSet.append(methlist)

    # '*globalSet' is a list expression that contain a list of sets
    s = set.intersection(*globalSet)
    myList = list(s)
    print(len(myList))

    with open("smells_intersection.csv", "w") as new:
        wr = csv.writer(new)
        wr.writerow(myList)

    print("Done ... save in smells_intersection.csv !")

def main():
    parser = argparse.ArgumentParser(description="Description")
    parser.add_argument("files",
                        help="Take csv files",
                        nargs = "+")

    args = parser.parse_args()

    readCsv(args.files)

if __name__ == "__main__":
    main()
