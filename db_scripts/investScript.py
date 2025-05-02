import sqlite3
import base64
import io
import matplotlib
import matplotlib.pyplot as plt
from db_scripts.consts import dbPath, SPVstockPath

matplotlib.use("Agg")


def CheckDB():
    try:
        with sqlite3.connect(dbPath) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM investPB")
            c.execute("SELECT * FROM investTransaction")
            c.execute("SELECT * FROM investStockPrice")
            return 0
    except sqlite3.OperationalError:
        print("Invest tables not found! Update the database structure!")
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
            """SELECT CASE WHEN name = ? AND stock = ? THEN 1 ELSE 0 END
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
            """INSERT INTO investPB (name, stock)
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
    # if fromApi:
    #     pass
    # else:
    #     pass
    print("Delete function not implemented yet!")
    return 0


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
    fee = round(float(tokens[7]), 2)
    stockPrice = 0

    if currency == "RON":
        stockPrice = round(
            (amount if amount > 0 else -amount)
            / (iAmount if iAmount > 0 else -iAmount),
            2,
        )

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
                WHERE person_bank = ? AND currency = ?
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
            INSERT INTO investTransaction VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
                         """
        stockpriceLine = date + "," + stock + "," + str(stockPrice)

        c.execute(standardQuery, (date, category, category, pb, amount, currency))
        c.execute(
            investQuery, (date, pb, amount, currency, ipbName, iAmount, stock, fee)
        )

        if fee != 0:
            c.execute(
                standardQuery,
                (date, "bank taxes", "invest taxes", pb, -fee, currency),
            )

        if stockPrice != 0:
            AddInvestStockPrice(stockpriceLine)

        conn.commit()

        return 0


def AddInvestStockPrice(line):
    if CheckDB() == -1:
        return -1

    tokens = line.split(",")
    date = tokens[0]
    stock = tokens[1]
    price = round(float(tokens[2]), 2)

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        # prepare statement for invest transactions
        investQuery = """
            INSERT INTO investStockPrice VALUES (NULL, ?, ?, ?)
                         """

        c.execute(investQuery, (date, stock, price))

        conn.commit()

        return 0


def ReadInvest(flag):
    if CheckDB() == -1:
        return -1

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        if flag == "alli":
            c.execute("SELECT * FROM investTransaction ORDER BY date DESC, id DESC")
            return c.fetchall()
        elif flag == "ipb":
            c.execute("SELECT * FROM investPB")
            return c.fetchall()
        elif flag == "retipb":
            c.execute("SELECT DISTINCT name FROM investPB ORDER BY name ASC")
            return [row[0] for row in c.fetchall()]
        elif flag == "stock":
            c.execute("SELECT * FROM investStockPrice ORDER BY date DESC, id DESC")
            return c.fetchall()
        elif flag == "graphstock":
            c.execute("SELECT * FROM investStockPrice ORDER BY date ASC, id ASC")
            return c.fetchall()
        elif flag == "ibal":
            c.execute(
                """
                SELECT 
                    investPB,
                    SUM(investAmount),
                    stock
                FROM 
                    investTransaction
                GROUP BY 
                    investPB, stock
                ORDER BY 
                    investPB, stock
                      """
            )
            return c.fetchall()
        else:
            raise ValueError("Invalid flag value.")


def GetTransactionHistory():
    if CheckDB() == -1:
        return -1

    data = ReadInvest("alli")
    finalHistory = []

    for row in data:
        id = row[0]
        date = row[1]
        pb = row[2]
        amount = row[3]
        currency = row[4]
        ipb = row[5]
        iAmount = row[6]
        stock = row[7]
        fee = row[8]

        stockPrice = (amount if amount > 0 else -amount) / (
            iAmount if iAmount > 0 else -iAmount
        )

        fRow = (
            id,
            date,
            pb,
            amount,
            currency,
            ipb,
            iAmount,
            stock,
            fee,
            round(stockPrice, 2),
        )
        finalHistory.append(fRow)

    return tuple(finalHistory)


def CalculateBalance():
    if CheckDB() == -1:
        return -1

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        stockBalance = ReadInvest("ibal")
        finalBalance = []

        # Calculate balance for each stock
        for row in stockBalance:
            investPB = row[0]
            investAmount = row[1]
            stock = row[2]

            # Find the price for the stock
            c.execute(
                """
                SELECT price 
                FROM investStockPrice 
                WHERE stock = ? 
                ORDER BY date DESC, id DESC 
                LIMIT 1
                """,
                (stock,),
            )
            priceRow = c.fetchone()
            if priceRow:
                price = priceRow[0]

            else:
                print(f"No price found for {stock}.")
                price = 1

            balance = round(investAmount * price, 2)

            finalBalance.append(
                {
                    "investPB": investPB,
                    "stock": stock,
                    "investAmount": round(investAmount, 6),
                    "balance": balance,
                }
            )

        return finalBalance


def GraphStockPrice():
    data = ReadInvest("graphstock")
    stock_data = {}

    # Group data by stock
    for row in data:
        stock_name = row[2]
        if stock_name not in stock_data:
            stock_data[stock_name] = {"dates": [], "prices": []}
        stock_data[stock_name]["dates"].append(row[1])
        stock_data[stock_name]["prices"].append(row[3])

    plt.clf()
    plt.figure(figsize=(12, 6))

    # Plot each stock separately
    for stock_name, values in stock_data.items():
        plt.plot(
            values["dates"],
            values["prices"],
            marker="o",
            linestyle="-",
            label=stock_name,
        )

    plt.title("Stock Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()
    plt.tight_layout()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)

    # Encode image to base64 string
    img_tag = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return img_tag
