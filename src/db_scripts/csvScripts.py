import csv
import os
from db_scripts.consts import *


def read_csv(file_name):
    values = []
    try:
        with open(file_name, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    values.append(row[0])
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    return values


def SPVconf(pth, new_SPV):
    # Function for configuring categories and currencies
    if pth == "inccat":
        path = SPVcatIncPath
    elif pth == "expcat":
        path = SPVcatExpPath
    elif pth == "subcat":
        path = SPVsubcatPath
    elif pth == "curr":
        path = SPVcurrPath

    with open(path, mode="w", newline="") as file:
        csvWriter = csv.writer(file)
        for i in new_SPV:
            csvWriter.writerow([i])
        return "Success!"


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
