import csv
import os
from db_scripts.consts import *
from helpers.configScripts import ModifyConfigLists


def read_spv(file_name):
    # Check if new format const exists
    if file_name == SPVcatExpPath:
        if expCategories is not None:
            return expCategories
    elif file_name == SPVcatIncPath:
        if incCategories is not None:
            return incCategories
    elif file_name == SPVsubcatPath:
        if subCategories is not None:
            return subCategories
    elif file_name == SPVcurrPath:
        if currencies is not None:
            return currencies
    else:
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


def SPVconf(param, new_SPV):
    # Function for configuring categories and currencies
    ModifyConfigLists(param, new_SPV)

    return 0

    # Old csv format handling
    # with open(path, mode="w", newline="") as file:
    #     csvWriter = csv.writer(file)
    #     for i in new_SPV:
    #         csvWriter.writerow([i])
    #     return 0


# def ShowExistingSPV(x):
#     if x == "catinc":
#         path = SPVcatIncPath
#     elif x == "catexp":
#         path = SPVcatExpPath
#     elif x == "subcat":
#         path = SPVsubcatPath
#     elif x == "curr":
#         path = SPVcurrPath

#     if os.path.exists(path):
#         with open(path, mode="r") as file:
#             csvFile = csv.reader(file)
#             print("Exisitng values:\n")
#             for lines in csvFile:
#                 print(lines)
#     else:
#         print("No values found.\n")
