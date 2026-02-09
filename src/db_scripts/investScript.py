import sqlite3
from db_scripts.consts import dbPath
from db_scripts import consts


def InitInvestPB(name, stock):
    # Person_bank initialization function
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        c.execute(
            "SELECT 1 FROM investPB WHERE name = ? AND stock = ?",
            (name, stock),
        )
        exists = c.fetchone()
        if exists != None:
            raise Exception("Account name with this stock already exists!")
        else:
            c.execute(
                "INSERT INTO investPB (name, stock) VALUES (?, ?)",
                (name, stock),
            )

        conn.commit()

    return


def AddInvestTransaction(dict):
    date = dict["date"]
    pb = dict["pb"]
    amount = round(float(dict["amount"]), 2)
    currency = dict["currency"]
    ipbName = dict["ipb"]
    iAmount = round(float(dict["stockAmount"]), 6)
    stock = dict["stock"]
    fee = round(float(dict["fee"]), 2)
    isReflective = dict["isReflective"]
    stockPrice = {"date": date, "stock": stock, "stockPrice": 0, "currency": currency}

    if currency == consts.mainCurrency:
        stockPrice["stockPrice"] = round(
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
        subCategory = ""
        if iAmount < 0:
            category, subCategory = "invest income"
        else:
            category = "invest expense"

        # prepare statements for standard and invest transactions
        standardQuery = """
            INSERT INTO main VALUES (NULL, ?, ?, ?, ?, ?, ?, "")
                         """
        investQuery = """
            INSERT INTO investTransaction VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
                         """

        c.execute(
            investQuery, (date, pb, amount, currency, ipbName, iAmount, stock, fee)
        )
        if isReflective:
            c.execute(
                standardQuery, (date, category, subCategory, pb, amount, currency)
            )

            if fee != 0:
                c.execute(
                    standardQuery,
                    (date, "bank taxes", "invest taxes", pb, -fee, currency),
                )

        conn.commit()

    if stockPrice["stockPrice"] != 0:
        AddInvestStockPrice(stockPrice)


def AddInvestStockPrice(stockData):
    date = stockData["date"]
    stock = stockData["stock"]
    price = round(float(stockData["stockPrice"]), 2)
    currency = stockData["currency"]

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        # prepare statement for invest transactions
        investQuery = """
            INSERT INTO investStockPrice VALUES (NULL, ?, ?, ?, ?)
                         """

        c.execute(investQuery, (date, stock, price, currency))

        conn.commit()

        return 0


def ReadInvest(flag):
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        if flag == "alli":
            c.execute(
                "SELECT * FROM investTransaction ORDER BY date DESC, id DESC",
            )
            return c.fetchall()
        elif flag == "ipb":
            c.execute("SELECT DISTINCT name FROM investPB ORDER BY name ASC")
            return [row[0] for row in c.fetchall()]
        elif flag == "stock":
            c.execute(
                "SELECT * FROM investStockPrice ORDER BY date DESC, id DESC",
            )
            return c.fetchall()
        elif flag == "graphstock":
            c.execute(
                "SELECT * FROM investStockPrice ORDER BY date ASC, id ASC",
            )
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


def GetInvestTransactionHistory(type):
    finalHistory = []

    if type == "main":
        data = ReadInvest("alli")
    elif type == "stock":
        data = ReadInvest("stock")

    if type == "main":
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
            finalHistory.append(
                [
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
                ]
            )
    elif type == "stock":
        for row in data:
            id = row[0]
            date = row[1]
            stock = row[2]
            price = row[3]
            currency = row[4]

            finalHistory.append(
                [
                    id,
                    date,
                    stock,
                    price,
                    currency
                ]
            )

    return finalHistory


def CalculateBalance():
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
                WHERE stock = ? AND currency = ?
                ORDER BY date DESC, id DESC 
                LIMIT 1
                """,
                (stock, consts.mainCurrency),
            )
            priceRow = c.fetchone()
            if priceRow:
                price = priceRow[0]

            else:
                print(f"No price found for {stock}.")
                price = 1

            balance = round(investAmount * price, 2)

            finalBalance.append(
                [
                    investPB,
                    stock,
                    round(investAmount, 6),
                    balance,
                ]
            )

        return finalBalance
