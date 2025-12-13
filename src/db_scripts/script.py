import sqlite3
from datetime import datetime
from db_scripts.baseScripts import Read, MarkerRead, ReadLegacy
import db_scripts.consts as consts
from db_scripts.SPVScripts import read_spv


def UpdateRecord(inp, mode):
    # Update record with received input
    with sqlite3.connect(consts.dbPath) as conn:
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


def GetYearlyData(x, year):
    if x == "yeartotalrep":

        result = []
        rows = Read("yeartotal")

        monthly_data = {}

        for row in rows:
            month = row[0]  # month in 'YYYY-MM' format
            date = row[1]  # transaction date
            amount = row[2]  # amount of the transaction
            currency = row[3]  # currency of the transaction

            # Convert the amount to main currency
            amount_in_currency = ConvertTo(currency, amount, date)

            # Initialize the month entry if not already present
            if month not in monthly_data:
                monthly_data[month] = {"expense": 0, "income": 0, "total": 0}

            # Categorize as expense or income
            if amount < 0:
                monthly_data[month]["expense"] += abs(
                    amount_in_currency
                )  # sum of expenses in main currency (absolute value)
            else:
                monthly_data[month][
                    "income"
                ] += amount_in_currency  # sum of income in main currency

            # Update the total (income - expense)
            monthly_data[month]["total"] += amount_in_currency

        # Convert monthly_data dictionary into a list of tuples
        for month, data in monthly_data.items():
            # Prepare the tuple for each month: (month, expense_in_currency, income_in_currency, total_in_currency)
            month_tuple = (
                month,
                int(data["income"]),  # income in main currency
                int(data["expense"]),  # expense in main currency
                int(data["total"]),  # total in main currency
            )
            result.append(month_tuple)

        return result

    elif x == "yearexprep":
        result = []
        rows = Read("yearexp")
        currencies = read_spv(consts.SPVcurrPath)
        monthly_data = {}

        for row in rows:
            month = row[0]
            currency = row[1]
            amount = row[2]
            date = row[3]

            # Initialize monthly data structure
            if month not in monthly_data:
                monthly_data[month] = {curr: 0 for curr in currencies}
                monthly_data[month]["total_in_currency"] = 0

            if currency in currencies:
                # Sum original amount per currency
                monthly_data[month][currency] += amount

                # Convert to main currency using exact date
                total_in_currency = ConvertTo(currency, amount, date)
                monthly_data[month]["total_in_currency"] += total_in_currency

        # Prepare final output
        for month in sorted(monthly_data.keys()):
            month_tuple = (
                (month,)
                + tuple(int(monthly_data[month][currency]) for currency in currencies)
                + (int(monthly_data[month]["total_in_currency"]),)
            )
            result.append(month_tuple)

        return result

    elif x == "yearincrep":
        result = []
        rows = Read("yearinc")
        currencies = read_spv(consts.SPVcurrPath)
        monthly_data = {}

        for row in rows:
            month = row[0]
            currency = row[1]
            amount = row[2]
            date = row[3]

            # Initialize monthly data structure
            if month not in monthly_data:
                monthly_data[month] = {curr: 0 for curr in currencies}
                monthly_data[month]["total_in_currency"] = 0

            if currency in currencies:
                # Sum original amount per currency
                monthly_data[month][currency] += amount

                # Convert to RON using exact date
                total_in_currency = ConvertTo(currency, amount, date)
                monthly_data[month]["total_in_currency"] += total_in_currency

        # Prepare final output
        for month in sorted(monthly_data.keys()):
            month_tuple = (
                (month,)
                + tuple(int(monthly_data[month][currency]) for currency in currencies)
                + (int(monthly_data[month]["total_in_currency"]),)
            )
            result.append(month_tuple)

        return result


def GetTransactionHistory(type):
    year = consts.currentYear
    Finalhistory = []

    if type == "expense":
        data = Read("m-", year)
    elif type == "income":
        data = Read("m+", year)
    elif type == "transfer":
        data = Read("alltran", year)
    elif type == "advtransfer":
        data = Read("alladvtran", year)
    elif type == "depositO":
        data = Read("opendep", year)
    elif type == "depositC":
        data = Read("closeddep", year)
    elif type == "currencyrates":
        if consts.isLegacyCurrencyRates:
            data = ReadLegacy("currrate")
        else:
            data = Read("currrate", year)

    if type == "expense":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                [
                    row_list[0],  # id
                    row_list[1],  # date
                    row_list[2],  # category
                    row_list[3],  # sub_category
                    row_list[4],  # pb
                    round(-row_list[5], 2),  # sum
                    row_list[6],  # currency
                    row_list[7],  # comment
                ]
            )

    elif type == "income":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                [
                    row_list[0],  # id
                    row_list[1],  # date
                    row_list[2],  # category
                    row_list[3],  # pb
                    round(row_list[4], 2),  # sum
                    row_list[5],  # currency
                    row_list[6],  # comment
                ]
            )

    elif type == "transfer":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                [
                    row_list[0],  # id
                    row_list[1],  # date
                    row_list[2],  # pb_from
                    row_list[3],  # pb_to
                    round(row_list[4], 2),  # sum
                    row_list[5],  # currency
                    row_list[6],  # comment
                ]
            )

    elif type == "advtransfer":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                [
                    row_list[0],  # id
                    row_list[1],  # date
                    row_list[2],  # pb_from
                    round(row_list[3], 2),  # sum_from
                    row_list[4],  # currency_from
                    row_list[5],  # pb_to
                    round(row_list[6], 2),  # sum_to
                    row_list[7],  # currency_to
                    (
                        round(row_list[8], 4) if row_list[8] != "" else ""
                    ),  # currency_rate
                    row_list[9],  # comment
                ]
            )

    elif type == "depositO" or type == "depositC":
        for row in data:
            row_list = list(row)
            Finalhistory.append(
                [
                    row_list[0],  # date_in
                    row_list[1],  # id
                    row_list[2],  # owner
                    round(row_list[3], 2),  # sum
                    row_list[4],  # currency
                    row_list[5],  # months
                    row_list[6],  # date_out
                    round(row_list[7], 2),  # percent
                    round(row_list[8], 4),  # currency_rate
                    round(row_list[9], 2),  # expect
                    row_list[10],  # comment
                ]
            )

    elif type == "currencyrates":
        if consts.isLegacyCurrencyRates:
            for row in data:
                row_list = list(row)
                Finalhistory.append(
                    [
                        row_list[0],  # date
                        row_list[1],  # currency
                        round(row_list[2], 4),  # rate
                    ]
                )
        else:
            for row in data:
                row_list = list(row)
                Finalhistory.append(
                    [
                        row_list[0],  # id
                        row_list[1],  # date
                        row_list[2],  # currency_M
                        row_list[3],  # currency_S
                        round(row_list[4], 4),  # rate
                    ]
                )

    return Finalhistory


def GenerateTable(flag):
    currentYear = consts.currentYear
    with sqlite3.connect(consts.dbPath) as conn:
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
                SELECT person_bank, currency, sum FROM main WHERE strftime('%Y', "date") = ?
                UNION ALL
                SELECT person_bank, currency, sum FROM Init_PB
                UNION ALL
                SELECT person_bank_from AS person_bank, currency, -sum FROM transfer WHERE strftime('%Y', "date") = ?
                UNION ALL
                SELECT person_bank_from AS person_bank, currency_from AS currency, -sum_from AS sum FROM advtransfer WHERE strftime('%Y', "date") = ?
                UNION ALL
                SELECT person_bank_to AS person_bank, currency_to AS currency, sum_to AS sum FROM advtransfer WHERE strftime('%Y', "date") = ?
                UNION ALL
                SELECT person_bank_to AS person_bank, currency, sum FROM transfer WHERE strftime('%Y', "date") = ?
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
                SELECT person_bank, currency, sum FROM main WHERE strftime('%Y', "date") = ?
                UNION ALL
                SELECT person_bank, currency, sum FROM Init_PB
                UNION ALL
                SELECT person_bank_from AS person_bank, currency, -sum FROM transfer WHERE strftime('%Y', "date") = ?
                UNION ALL
                SELECT person_bank_from AS person_bank, currency_from AS currency, -sum_from AS sum FROM advtransfer WHERE strftime('%Y', "date") = ?
                UNION ALL
                SELECT person_bank_to AS person_bank, currency_to AS currency, sum_to AS sum FROM advtransfer WHERE strftime('%Y', "date") = ?
                UNION ALL
                SELECT person_bank_to AS person_bank, currency, sum FROM transfer WHERE strftime('%Y', "date") = ?
                -- PBD logic
                UNION ALL
                SELECT owner AS person_bank, currency, -sum FROM deposit WHERE isOpen = 1
            ) p 
            JOIN Marker_type mt ON p.person_bank = mt.bank_rec
            GROUP BY p.currency, mt.type
            ORDER BY p.currency, mt.type
        """

        else:
            return []

        return c.execute(
            query, (currentYear, currentYear, currentYear, currentYear, currentYear)
        ).fetchall()


def read_and_convert_data(x, mode, cursor):
    current_date = datetime.now().strftime("%Y-%m-%d")

    if x == "norm":
        data = Read(mode, consts.currentYear)
    else:
        data = MarkerRead(mode, x)
    modified_dict = {}

    if mode == "allcurr":
        for row in data:
            row_list = list(row)
            currency = row_list[0]
            amount = row_list[1]

            converted_amount = ConvertTo(currency, amount, current_date, cursor)

            modified_dict[currency] = converted_amount

    else:
        for row in data:
            row_list = list(row)
            owner = row_list[0]
            amount = row_list[1]
            currency_column = row_list[2]

            converted_amount = ConvertTo(currency_column, amount, current_date, cursor)

            if owner in modified_dict:
                modified_dict[owner] += converted_amount
            else:
                modified_dict[owner] = converted_amount

    return modified_dict


def ConvRead(x, mode, include_percentage=False):
    with sqlite3.connect(consts.dbPath) as conn:
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
    with sqlite3.connect(consts.dbPath) as conn:
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

            converted_amount = ConvertTo(currency_column, amount, current_date, c)

            # Append the tuple with the converted amount
            modified_list.append((owner, currency_column, amount, converted_amount))

    return modified_list


def GenerateReport(rType, rFormat, categoryFilter, year):
    # Function for generating table_data for reports page
    table_data = {"table_dict": {}, "total": []}
    # Months lsit
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    queryCat = """
                    SELECT category, sum, currency, date FROM main 
                    WHERE strftime('%m', date) = ? AND category = ? AND strftime('%Y', date) = ?
                    """
    querySubcat = """
                    SELECT sub_category, sum, currency, date FROM main 
                    WHERE strftime('%m', date) = ? AND sub_category = ? AND category = ? AND strftime('%Y', date) = ?
                    """
    querySubcat_noCat = """
                    SELECT sub_category, sum, currency, date FROM main 
                    WHERE strftime('%m', date) = ? AND sub_category = ? AND strftime('%Y', date) = ?
                    """

    with sqlite3.connect(consts.dbPath) as conn:
        c = conn.cursor()

        table_data["report_type"] = rType
        table_data["report_format"] = rFormat

        if rType == "inccat":
            catList = Read("retcat+")
        elif rType == "expcat":
            catList = Read("retcat-")
        elif rType == "subcat" and categoryFilter == "all":
            c.execute(
                """
                      SELECT DISTINCT sub_category FROM main
                      WHERE sum < 0
                      ORDER BY sub_category DESC
                      """
            )
            catList = [row[0] for row in c.fetchall()]
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
                    if categoryFilter == "all":
                        c.execute(querySubcat_noCat, (month, cat, year))
                    else:
                        c.execute(querySubcat, (month, cat, categoryFilter, year))
                else:
                    c.execute(queryCat, (month, cat, year))

                data = c.fetchall()
                converted = []

                if data:
                    for row in data:
                        category, amount, currency, date = row
                        amount = abs(round(amount, 2))
                        convertedAmount = ConvertTo(currency, amount, date, c)
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
    with sqlite3.connect(consts.dbPath) as conn:
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

                converted_amount = ConvertTo(currency, amount, date, c)

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

                converted_amount = ConvertTo(currency, amount, date, c)

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

        # elif type == "catincbankrep":
        #     categories_df = pd.read_csv(SPVcatIncPath, header=None)
        #     categories_list = categories_df[0].tolist()

        #     query = """
        #     SELECT category, person_bank, currency, ROUND(SUM(sum), 2)
        #     FROM main
        #     WHERE category IN ({})
        #     AND strftime("%m", date) = ?
        #     GROUP BY category, person_bank
        #     ORDER BY category, person_bank DESC
        #     """.format(
        #         ",".join("?" for _ in categories_list)
        #     )

        #     params = categories_list + [month]
        #     c.execute(query, params)

        #     return c.fetchall()

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

                converted_amount = ConvertTo(currency, amount, date, c)

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


def ConvertTo(currency, amount, date, c=None):
    if c is None:
        conn = sqlite3.connect(consts.dbPath)
        c = conn.cursor()

    if consts.isLegacyCurrencyRates:
        return ConvertToRON(currency, amount, date, c)
    else:
        if currency != consts.mainCurrency:
            query = """
                SELECT rate 
                FROM exc_rate 
                WHERE currency_M = ? AND currency_S = ?
                ORDER BY ABS(JULIANDAY(date) - JULIANDAY(?))
                LIMIT 1
            """
            c.execute(query, (consts.mainCurrency, currency, date))
            excRate_row = c.fetchone()
            if excRate_row != None:
                excRate = excRate_row[0]  # Extract the exchange rate
            else:
                excRate = 1
        else:
            excRate = 1
        converted_amount = int(amount * excRate)

        return converted_amount


def ConvertToRON(currency, amount, date, c=None):
    # Converting to RON

    if c is None:
        conn = sqlite3.connect(consts.dbPath)
        c = conn.cursor()

    if currency != "RON":
        query = """
            SELECT rate 
            FROM exc_rate 
            WHERE currency = ?
            ORDER BY ABS(JULIANDAY(date) - JULIANDAY(?))
            LIMIT 1
        """
        c.execute(query, (currency, date))
        excRate_row = c.fetchone()
        if excRate_row != None:
            excRate = excRate_row[0]  # Extract the exchange rate
        else:
            excRate = 1
    else:
        excRate = 1
    converted_amount = int(amount * excRate)

    return converted_amount
