import csv
import os
import db_scripts.consts as consts
from helpers.configScripts import ModifyConfigLists


def read_spv(file_name):
    # Check if new format const exists
    if file_name == consts.SPVcatExpPath:
        if consts.expCategories is not None and consts.expCategories:
            return consts.expCategories
    elif file_name == consts.SPVcatIncPath:
        if consts.incCategories is not None and consts.incCategories:
            return consts.incCategories
    elif file_name == consts.SPVsubcatPath:
        if consts.subCategories is not None and consts.subCategories:
            return consts.subCategories
    elif file_name == consts.SPVcurrPath:
        if consts.currencies is not None and consts.currencies:
            return consts.currencies

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
