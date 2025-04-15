import sqlite3
from datetime import datetime
from db_scripts.consts import *


def CheckDB():
    try:
        with sqlite3.connect(dbPath) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM investPB")
            c.execute("SELECT * FROM investTransaction")
            c.execute("SELECT * FROM investStockPrice")
            return 0
    except sqlite3.OperationalError:
        print("Invest table not found! Update the database structure!")
        return -1


def ManageIPB(command, ipbName=""):
    if CheckDB() == -1:
        return
    if command == "add":
        AddIPB()
    elif command == "update":
        UpdateIPB(ipbName)
    elif command == "delete":
        DeleteIPB(ipbName)


def AddIPB(fromAPI=False, line=None):
    if fromAPI:
        if CheckDB() == -1:
            return -1
        tokens = line.split(",")
        ipbName = tokens[0]
        ipbStock = tokens[1]

    else:
        ipbName = input("Enter the name of the investment portfolio: ")
        ipbStock = input("Enter the stock symbol name: ")

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()
        # Check if the investment account already exists
        c.execute(
            """SELECT CASE(WHEN name = ? AND stock = ? THEN 1 ELSE 0 END)
            FROM investPB
            WHERE name = ?""",
            (ipbName, ipbStock, ipbName),
        )
        row = c.fetchall()
        if any(r[0] == 1 for r in row):
            print("Investment portfolio already exists!")
            return -2
        # Insert the investment account into the database
        c.execute(
            """INSERT INTO investPB (name, stock
            VALUES (?, ?)""",
            (ipbName, ipbStock),
        )
        conn.commit()
        print(f"Investment portfolio '{ipbName}' added successfully!")
    return 0


def UpdateIPB(ipbName, fromAPI=False, line=None):
    if fromAPI:
        if CheckDB() == -1:
            return -1
        tokens = line.split(",")
        ipbName = tokens[0]
        ipbStock = tokens[1]
        ipbNameNew = tokens[2]
        ipbStockNew = tokens[3]

    else:
        ipbName = input("Enter the name of the investment portfolio: ")
        ipbStock = input("Enter the stock symbol name: ")
        ipbNameNew = input("Enter the new name of the investment portfolio: ")
        ipbStockNew = input("Enter the new stock symbol name: ")

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()
        # Check if the investment account exists
        c.execute(
            """SELECT EXISTS(
            SELECT 1 FROM investPB 
            WHERE name = ? AND stock = ?
            )""",
            (ipbName, ipbStock),
        )
        exists = c.fetchone()[0]
        if not exists:
            print("No record found for the given investment portfolio!")
            return

        # Update the investment account in the database
        c.execute(
            """UPDATE investPB SET stock = ? WHERE name = ?""",
            (ipbStockNew, ipbNameNew),
        )
        conn.commit()
        print(
            f"Investment portfolio '{ipbName}' -> '{ipbNameNew}' updated successfully!"
        )
    return 0


def DeleteIPB(ipbName, fromApi=False):
    # TODO: Add delete process
    if fromApi:
        pass
    else:
        pass


def AddInvestTransaction(line):
    if CheckDB() == -1:
        return -1

    tokens = line.split(",")
    date = tokens[0]
    pb = tokens[1]
    amount = round(float(tokens[2]), 2)
    currency = tokens[3]
    ipbName = tokens[4]
    iAmount = round(float(tokens[5]), 6)
    stock = tokens[6]

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        # check if investment account exists
        c.execute(
            """SELECT EXISTS(
            SELECT 1 FROM investPB 
            WHERE name = ? AND stock = ?
            )""",
            (ipbName, stock),
        )
        investExists = c.fetchone()[0]
        if investExists:
            # check if standard account exists
            c.execute(
                """SELECT EXISTS(
                SELECT 1 FROM Init_PB 
                WHERE pb = ? AND currency = ?
                )""",
                (pb, currency),
            )
            standardExists = c.fetchone()[0]
            if not standardExists:
                raise Exception(
                    f"Standard account '{pb}' with currency '{currency}' does not exist!"
                )
        else:
            raise Exception(
                f"Investment account '{ipbName}' with stock '{stock}' does not exist!"
            )

        # check if transaction is positive or negative
        category = ""
        if iAmount < 0:
            category = "invest income"
        else:
            category = "invest expense"

        # prepare statements for standard and invest transactions
        standardQuery = """
            INSERT INTO main VALUES (NULL, ?, ?, ?, ?, ?, ?, "")
                         """
        investQuery = """
            INSERT INTO investTransaction VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
                         """

        c.execute(standardQuery, (date, category, category, pb, amount, currency))
        c.execute(investQuery, (date, pb, amount, currency, ipbName, iAmount, stock))

        conn.commit()
    return 0
