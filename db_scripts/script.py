import sqlite3
import pandas as pd
from datetime import datetime
from db_scripts.baseScripts import Read, MarkerRead
from db_scripts.consts import *
from db_scripts.csvScripts import read_csv


def UpdateRecord(inp, mode):
    # Update record with received input
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        inp = inp.split(",")
        if mode == "main":
            c.execute(
                "UPDATE main SET date = ?, category = ?, sub_category = ?, person_bank = ?, sum = ?, currency = ?, comment = ? WHERE id = ?",
                (inp[1], inp[2], inp[3], inp[4], inp[5], inp[6], inp[7], int(inp[0])),
            )
        elif mode == "transfer":
            c.execute(
                "UPDATE transfer SET date = ?, person_bank_from = ?, person_bank_to = ?, sum = ?, currency = ?, comment = ? WHERE id = ?",
                (inp[1], inp[2], inp[3], inp[4], inp[5], inp[6], int(inp[0])),
            )
        elif mode == "advtransfer":
            c.execute(
                "UPDATE advtransfer SET date = ?, person_bank_from = ?, sum_from = ?, currency_from = ?, person_bank_to = ?, sum_to = ?, currency_to = ?, currency_rate = ?, comment = ? WHERE id = ?",
                (
                    inp[1],
                    inp[2],
                    inp[3],
                    inp[4],
                    inp[5],
                    inp[6],
                    inp[7],
                    inp[8],
                    inp[9],
                    int(inp[0]),
                ),
            )

        conn.commit()


def GetYearlyData(x):
    if x == "yeartotalrep":

        result = []
        rows = Read("yeartotal")

        monthly_data = {}

        for row in rows:
            month = row[0]  # month in 'YYYY-MM' format
            date = row[1]  # transaction date
            amount = row[2]  # amount of the transaction
            currency = row[3]  # currency of the transaction

            # Convert the amount to RON
            amount_in_ron = ConvertToRON(currency, amount, date)

            # Initialize the month entry if not already present
            if month not in monthly_data:
                monthly_data[month] = {"expense": 0, "income": 0, "total": 0}

            # Categorize as expense or income
            if amount < 0:
                monthly_data[month]["expense"] += abs(
                    amount_in_ron
                )  # sum of expenses in RON (absolute value)
            else:
                monthly_data[month]["income"] += amount_in_ron  # sum of income in RON

            # Update the total (income - expense)
            monthly_data[month]["total"] += amount_in_ron

        # Convert monthly_data dictionary into a list of tuples
        for month, data in monthly_data.items():
            # Prepare the tuple for each month: (month, expense_in_RON, income_in_RON, total_in_RON)
            month_tuple = (
                month,
                int(data["income"]),  # income in RON
                int(data["expense"]),  # expense in RON
                int(data["total"]),  # total in RON
            )
            result.append(month_tuple)

        return result

    elif x == "yearexprep":
        result = []
        rows = Read("yearexp")
        currencies = read_csv(SPVcurrPath)
        monthly_data = {}

        for row in rows:
            month = row[0]
            currency = row[1]
            amount = row[2]
            date = row[3]

            # Initialize monthly data structure
            if month not in monthly_data:
                monthly_data[month] = {curr: 0 for curr in currencies}
                monthly_data[month]["total_in_RON"] = 0

            if currency in currencies:
                # Sum original amount per currency
                monthly_data[month][currency] += amount

                # Convert to RON using exact date
                total_in_RON = ConvertToRON(currency, amount, date)
                monthly_data[month]["total_in_RON"] += total_in_RON

        # Prepare final output
        for month in sorted(monthly_data.keys()):
            month_tuple = (
                (month,)
                + tuple(int(monthly_data[month][currency]) for currency in currencies)
                + (int(monthly_data[month]["total_in_RON"]),)
            )
            result.append(month_tuple)

        return result

    elif x == "yearincrep":
        result = []
        rows = Read("yearinc")
        currencies = read_csv(SPVcurrPath)
        monthly_data = {}

        for row in rows:
            month = row[0]
            currency = row[1]
            amount = row[2]
            date = row[3]

            # Initialize monthly data structure
            if month not in monthly_data:
                monthly_data[month] = {curr: 0 for curr in currencies}
                monthly_data[month]["total_in_RON"] = 0

            if currency in currencies:
                # Sum original amount per currency
                monthly_data[month][currency] += amount

                # Convert to RON using exact date
                total_in_RON = ConvertToRON(currency, amount, date)
                monthly_data[month]["total_in_RON"] += total_in_RON

        # Prepare final output
        for month in sorted(monthly_data.keys()):
            month_tuple = (
                (month,)
                + tuple(int(monthly_data[month][currency]) for currency in currencies)
                + (int(monthly_data[month]["total_in_RON"]),)
            )
            result.append(month_tuple)

        return result


def GetTransactionHistory(type):
    Finalhistory = []

    if type == "expense":
        data = Read("m-")
    elif type == "income":
        data = Read("m+")
    elif type == "transfer":
        data = Read("alltran")
    elif type == "advtransfer":
        data = Read("alladvtran")
    elif type == "depositO":
        data = Read("opendep")
    elif type == "depositC":
        data = Read("closeddep")

    if type == "expense":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                {
                    "id": row_list[0],
                    "date": row_list[1],
                    "category": row_list[2],
                    "sub_category": row_list[3],
                    "pb": row_list[4],
                    "sum": round(row_list[5], 2),
                    "currency": row_list[6],
                    "comment": row_list[7],
                }
            )

    elif type == "income":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                {
                    "id": row_list[0],
                    "date": row_list[1],
                    "category": row_list[2],
                    "pb": row_list[3],
                    "sum": round(row_list[4], 2),
                    "currency": row_list[5],
                    "comment": row_list[6],
                }
            )

    elif type == "transfer":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                {
                    "id": row_list[0],
                    "date": row_list[1],
                    "pb_from": row_list[2],
                    "pb_to": row_list[3],
                    "sum": round(row_list[4], 2),
                    "currency": row_list[5],
                    "comment": row_list[6],
                }
            )
            
    elif type == "advtransfer":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                {
                    "ADV_id": row_list[0],
                    "ADV_date": row_list[1],
                    "ADV_pb_from": row_list[2],
                    "ADV_sum_from": round(row_list[3], 2),
                    "ADV_currency_from": row_list[4],
                    "ADV_pb_to": row_list[5],
                    "ADV_sum_to": round(row_list[6], 2),
                    "ADV_currency_to": row_list[7],
                    "ADV_currency_rate": (
                        round(row_list[8], 4) if row_list[8] != "" else ""
                    ),
                    "ADV_comment": row_list[9],
                }
            )

    elif type == "depositO" or type == "depositC":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                {
                    "date_in": row_list[0],
                    "name": row_list[1],
                    "owner": row_list[2],
                    "sum": round(row_list[3], 2),
                    "currency": row_list[4],
                    "months": row_list[5],
                    "date_out": row_list[6],
                    "percent": round(row_list[7], 2),
                    "currency_rate": round(row_list[8], 4),
                    "expect": round(row_list[9], 2),
                    "comment": row_list[10],
                }
            )

    return Finalhistory


def GenerateTable(flag):
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()
        if flag == "currType":
            query = """
            SELECT 
                p.currency,
                mt.type,
                ROUND(SUM(p.sum), 2) as total_amount,
                ROUND(SUM(p.sum) * 100.0 / SUM(SUM(p.sum)) OVER (PARTITION BY p.currency), 2) as percentage
            FROM (
                -- Main accounts and transfers
                SELECT person_bank, currency, sum FROM main
                UNION ALL
                SELECT person_bank, currency, sum FROM Init_PB
                UNION ALL
                SELECT person_bank_from AS person_bank, currency, -sum FROM transfer
                UNION ALL
                SELECT person_bank_from AS person_bank, currency_from AS currency, -sum_from AS sum FROM advtransfer
                UNION ALL
                SELECT person_bank_to AS person_bank, currency_to AS currency, sum_to AS sum FROM advtransfer
                UNION ALL
                SELECT person_bank_to AS person_bank, currency, sum FROM transfer
                -- PBD logic
                UNION ALL
                SELECT owner AS person_bank, currency, -sum FROM deposit WHERE isOpen = 1
            ) p 
            JOIN Marker_type mt ON p.person_bank = mt.bank_rec
            GROUP BY mt.type, p.currency
            ORDER BY mt.type, p.currency
        """

        elif flag == "currType+%":
            query = """
            SELECT 
                p.currency,
                mt.type,
                ROUND(SUM(p.sum), 2) as total_amount,
                ROUND(SUM(p.sum) * 100.0 / SUM(SUM(p.sum)) OVER (PARTITION BY p.currency), 2) as percentage
            FROM (
                -- Main accounts and transfers
                SELECT person_bank, currency, sum FROM main
                UNION ALL
                SELECT person_bank, currency, sum FROM Init_PB
                UNION ALL
                SELECT person_bank_from AS person_bank, currency, -sum FROM transfer
                UNION ALL
                SELECT person_bank_from AS person_bank, currency_from AS currency, -sum_from AS sum FROM advtransfer
                UNION ALL
                SELECT person_bank_to AS person_bank, currency_to AS currency, sum_to AS sum FROM advtransfer
                UNION ALL
                SELECT person_bank_to AS person_bank, currency, sum FROM transfer
                -- PBD logic
                UNION ALL
                SELECT owner AS person_bank, currency, -sum FROM deposit WHERE isOpen = 1
            ) p 
            JOIN Marker_type mt ON p.person_bank = mt.bank_rec
            GROUP BY mt.type, p.currency
            ORDER BY mt.type, p.currency
        """

        else:
            return []

        return c.execute(query).fetchall()


def read_and_convert_data(x, mode, cursor):
    current_date = datetime.now().strftime("%Y-%m-%d")

    if x == "norm":
        data = Read(mode)
    else:
        data = MarkerRead(mode, x)
    modified_dict = {}

    if mode == "allcurr":
        for row in data:
            row_list = list(row)
            currency = row_list[0]
            amount = row_list[1]

            converted_amount = ConvertToRON(currency, amount, current_date, cursor)

            modified_dict[currency] = converted_amount

    else:
        for row in data:
            row_list = list(row)
            owner = row_list[0]
            amount = row_list[1]
            currency_column = row_list[2]

            converted_amount = ConvertToRON(
                currency_column, amount, current_date, cursor
            )

            if owner in modified_dict:
                modified_dict[owner] += converted_amount
            else:
                modified_dict[owner] = converted_amount

    return modified_dict


def ConvRead(x, mode, include_percentage=False):
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        modified_dict = read_and_convert_data(x, mode, c)

        # Calculate the total sum of all amounts
        total_sum = sum(modified_dict.values())

        # Convert the grouped data back into a list of tuples
        if include_percentage:
            modified_list = [
                (
                    owner,
                    round(total_amount, 2),
                    round((total_amount / total_sum) * 100, 2),
                )
                for owner, total_amount in modified_dict.items()
            ]
        else:
            modified_list = [
                (owner, round(total_amount, 2))
                for owner, total_amount in modified_dict.items()
            ]

    return modified_list


def ConvReadPlus(x, mode):
    # Function for reading DB and returning converted to RON amounts
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        current_date = datetime.now().strftime("%Y-%m-%d")

        if x == "norm":
            data = Read(mode)
        else:
            data = MarkerRead(mode, x)
        modified_list = []

        for row in data:
            row_list = list(row)
            owner = row_list[0]
            amount = round(row_list[1], 2)
            currency_column = row_list[2]

            converted_amount = ConvertToRON(currency_column, amount, current_date, c)

            # Append the tuple with the converted amount
            modified_list.append((owner, currency_column, amount, converted_amount))

    return modified_list


def GenerateReport(params):
    # Function for generating table_data for reports page
    table_data = {"table_dict": {}, "total": []}
    # Months lsit
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    queryCat = """
                    SELECT category, sum, currency, date FROM main 
                    WHERE strftime('%m', date) = ? AND category = ?
                    """
    querySubcat = """
                    SELECT sub_category, sum, currency, date FROM main 
                    WHERE strftime('%m', date) = ? AND sub_category = ? AND category = ?
                    """

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        temp = params.split(",")
        rType = temp[0]
        table_data["report_type"] = rType
        rFormat = temp[1]
        table_data["report_format"] = rFormat

        if rType == "subcat":
            categoryFilter = temp[2]

        if rType == "inccat":
            catList = Read("retcat+")
        elif rType == "expcat":
            catList = Read("retcat-")
        else:
            c.execute(
                """
                      SELECT DISTINCT sub_category FROM main
                      WHERE category IN (?) 
                      ORDER BY sub_category DESC
                      """,
                (categoryFilter,),
            )
            catList = [row[0] for row in c.fetchall()]

        for cat in catList:
            for month in months:
                if rType == "subcat":
                    c.execute(querySubcat, (month, cat, categoryFilter))
                else:
                    c.execute(queryCat, (month, cat))

                data = c.fetchall()
                converted = []

                if data:
                    for row in data:
                        category, amount, currency, date = row
                        amount = abs(round(amount, 2))
                        convertedAmount = ConvertToRON(currency, amount, date, c)
                        converted.append((category, convertedAmount))
                else:
                    converted.append((cat, 0))

                totalConverted = [converted[0][0], sum(row[1] for row in converted)]

                if totalConverted[0] in table_data["table_dict"]:
                    table_data["table_dict"][totalConverted[0]].append(
                        round(totalConverted[1], 2)
                    )
                else:
                    table_data["table_dict"][totalConverted[0]] = [
                        round(totalConverted[1], 2)
                    ]

        total = [0] * 12
        for values in table_data["table_dict"].values():
            for i in range(12):
                total[i] += values[i]

        total = [round(x, 2) for x in total]

        if rFormat == "ron":
            table_data["total"] = total

        elif rFormat == "percent":
            for category, values in table_data["table_dict"].items():
                for i in range(12):
                    if total[i] == 0:
                        table_data["table_dict"][category][i] = 0
                    else:
                        table_data["table_dict"][category][i] = int(
                            (values[i] / total[i]) * 100
                        )

    return table_data


def ReadAdv(type, month):
    # Special read function for reports with month selector
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        if type == "catpbrep":
            c.execute(
                """
                SELECT 
                    category,
                    person_bank, 
                    currency,
                    SUM(sum)
                FROM 
                    main
                WHERE 
                    strftime('%m', date) = ?
                GROUP BY 
                    person_bank, 
                    category, 
                    currency
                ORDER BY 
                    category DESC
                """,
                (month,),
            )
            return c.fetchall()

        elif type == "catincrep":
            catQuery = """
                SELECT DISTINCT category
                FROM main
                WHERE sum > 0"""
            c.execute(catQuery)
            categories_list = c.fetchall()
            categories_list = [cat[0] for cat in categories_list]

            query = """
            SELECT category, currency, sum, date
            FROM main
            WHERE category IN ({})
            AND strftime("%m", date) = ?
            ORDER BY category DESC
            """.format(
                ",".join("?" for _ in categories_list)
            )

            params = categories_list + [month]
            c.execute(query, params)
            data = c.fetchall()
            modified_dict = {}

            # Convert to RON using dynamic table
            for row in data:
                row_list = list(row)
                category = row_list[0]
                currency = row_list[1]
                amount = row_list[2]
                date = row_list[3]

                converted_amount = ConvertToRON(currency, amount, date, c)

                if category in modified_dict:
                    modified_dict[category] += converted_amount
                else:
                    modified_dict[category] = converted_amount

            # Calculate the total income in RON
            total_income = sum(modified_dict.values())

            # Convert the grouped data back into a list of tuples
            modified_list = [
                (
                    category,
                    int(total_amount),
                    f"{(total_amount / total_income) * 100:.0f}%",
                )
                for category, total_amount in modified_dict.items()
            ]

            return modified_list

        elif type == "catexprep":
            catQuery = """
                SELECT DISTINCT category
                FROM main
                WHERE sum < 0"""
            c.execute(catQuery)
            categories_list = c.fetchall()
            categories_list = [cat[0] for cat in categories_list]

            query = """
            SELECT category, currency, sum, date
            FROM main
            WHERE category IN ({})
            AND strftime("%m", date) = ?
            ORDER BY category DESC
            """.format(
                ",".join("?" for _ in categories_list)
            )

            params = categories_list + [month]
            c.execute(query, params)
            data = c.fetchall()
            modified_dict = {}

            # Convert to RON using dynamic table
            for row in data:
                row_list = list(row)
                category = row_list[0]
                currency = row_list[1]
                amount = row_list[2]
                date = row_list[3]

                converted_amount = ConvertToRON(currency, amount, date, c)

                if category in modified_dict:
                    modified_dict[category] += converted_amount
                else:
                    modified_dict[category] = converted_amount

            # Calculate the total expense in RON
            total_expense = sum(modified_dict.values())

            # Convert the grouped data back into a list of tuples
            modified_list = [
                (
                    category,
                    int(total_amount),
                    f"{(total_amount / total_expense) * 100:.0f}%",
                )
                for category, total_amount in modified_dict.items()
            ]

            return modified_list

        elif type == "catincbankrep":
            categories_df = pd.read_csv(SPVcatIncPath, header=None)
            categories_list = categories_df[0].tolist()

            query = """
            SELECT category, person_bank, currency, ROUND(SUM(sum), 2)
            FROM main
            WHERE category IN ({})
            AND strftime("%m", date) = ?
            GROUP BY category, person_bank
            ORDER BY category, person_bank DESC
            """.format(
                ",".join("?" for _ in categories_list)
            )

            params = categories_list + [month]
            c.execute(query, params)

            return c.fetchall()

        elif type == "subcatrep":
            subcatQuery = "SELECT DISTINCT sub_category FROM main WHERE sum < 0"
            subcatList = c.execute(subcatQuery).fetchall()
            subcatList = [subcat[0] for subcat in subcatList]

            query = """
            SELECT sub_category, currency, sum, date
            FROM main
            WHERE sub_category IN ({})
            AND strftime("%m", date) = ?
            ORDER BY sub_category DESC
            """.format(
                ",".join("?" for _ in subcatList)
            )

            params = subcatList + [month]
            c.execute(query, params)
            data = c.fetchall()
            modified_dict = {}

            # Convert to RON using dynamic table
            for row in data:
                row_list = list(row)
                subCategory = row_list[0]
                currency = row_list[1]
                amount = row_list[2]
                date = row_list[3]

                converted_amount = ConvertToRON(currency, amount, date, c)

                if subCategory in modified_dict:
                    modified_dict[subCategory] += converted_amount
                else:
                    modified_dict[subCategory] = converted_amount

            # Calculate the total in RON
            total_expense = sum(modified_dict.values())

            # Convert the grouped data back into a list of tuples
            modified_list = [
                (
                    subCategory,
                    int(total_amount),
                    f"{(total_amount / total_expense) * 100:.0f}%",
                )
                for subCategory, total_amount in modified_dict.items()
            ]

        return modified_list


def ConvertToRON(currency, amount, date, c = None):
    # Converting to RON
    
    if c is None:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()

    if currency != "RON":
        query = f"""
            SELECT {currency} 
            FROM exc_rate 
            WHERE {currency} != 0
            ORDER BY ABS(JULIANDAY(date) - JULIANDAY('{date}'))
            LIMIT 1
        """
        c.execute(query)
        excRate_row = c.fetchone()
        if excRate_row != None:
            excRate = excRate_row[0]  # Extract the exchange rate
        else:
            excRate = 1
    else:
        excRate = 1
    converted_amount = int(amount * excRate)

    return converted_amount
