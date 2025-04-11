import os.path
import sqlite3
from datetime import datetime
from db_scripts.consts import *


def ManageIPB(command, ipbName=""):
    try:
        with sqlite3.connect(dbPath) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM investPB")
    except sqlite3.OperationalError:
        print("Invest table not found! Update the database structure!")
        return
    if command == "add":
        AddIPB()
    elif command == "update":
        UpdateIPB(ipbName)
    elif command == "delete":
        DeleteIPB(ipbName)


def AddIPB(fromAPI=False):
    if fromAPI:
        # TODO: Add from API process
        pass
    else:
        ipbName = input("Enter the name of the investment portfolio: ")
        ipbStock = input("Enter the stock symbol name: ")

        with sqlite3.connect(dbPath) as conn:
            c = conn.cursor()
            # Check if the investment portfolio already exists
            c.execute(
                """SELECT CASE(WHEN name = ? AND stock = ? THEN 1 ELSE 0 END)
                FROM investPB
                WHERE name = ?""",
                (ipbName, ipbStock, ipbName),
            )
            row = c.fetchall()
            if any(r[0] == 1 for r in row):
                print("Investment portfolio already exists!")
                return
            # Insert the investment portfolio into the database
            c.execute(
                """INSERT INTO investPB (name, stock
                VALUES (?, ?)""",
                (ipbName, ipbStock),
            )
            conn.commit()

            print(f"Investment portfolio '{ipbName}' added successfully!")

def UpdateIPB(ipbName, fromAPI=False):
    # TODO: Add update process
    if fromAPI:
        pass
    else:
        pass
    
def DeleteIPB(ipbName, fromApi=False):
    # TODO: Add delete process
    if fromApi:
        pass
    else:
        pass