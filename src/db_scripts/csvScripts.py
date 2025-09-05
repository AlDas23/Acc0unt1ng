import csv
import os
from db_scripts.consts import *


def read_csv(file_name):
    values = []
    with open(file_name, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                values.append(row[0])
    return values


def SPVconf(pth, new_SPV, inpMode):
    # Function for configuring categories and currencies
    if pth == "catinc":
        path = SPVcatIncPath
    elif pth == "catexp":
        path = SPVcatExpPath
    elif pth == "subcat":
        path = SPVsubcatPath
    elif pth == "curr":
        path = SPVcurrPath

    new_SPV = new_SPV.split(",")

    if inpMode == "A" or inpMode == "a":
        new_SPV = "," + new_SPV
        with open(path, mode="a", newline="") as file:
            csvWriter = csv.writer(file)
            for i in new_SPV:
                csvWriter.writerow([i])
        return "Success!"

    elif inpMode == "R" or inpMode == "r":
        with open(path, mode="w", newline="") as file:
            csvWriter = csv.writer(file)
            for i in new_SPV:
                csvWriter.writerow([i])
        return "Success!"

    else:
        raise Exception("Unknown command! Expected A, a, R, r")


def ShowExistingSPV(x):
    if x == "catinc":
        path = SPVcatIncPath
    elif x == "catexp":
        path = SPVcatExpPath
    elif x == "subcat":
        path = SPVsubcatPath
    elif x == "curr":
        path = SPVcurrPath

    if os.path.exists(path):
        with open(path, mode="r") as file:
            csvFile = csv.reader(file)
            print("Exisitng values:\n")
            for lines in csvFile:
                print(lines)
    else:
        print("No values found.\n")
