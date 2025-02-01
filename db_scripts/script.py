import os.path
import io
import csv
import sqlite3
import pandas as pd
from datetime import datetime
from db_scripts.consts import *


def NewDBase():
    # Create or replace DB file using template
    directory = os.path.dirname(dbPath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(dbPath):
        os.remove(dbPath)

    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    c.execute(
        """CREATE TABLE main (
                id integer,
                date text,
                category text,
                sub_category text,
                person_bank text,
                sum real,
                currency text,
                comment text
            )"""
    )
    c.execute(
        """CREATE TABLE exc_rate (
                date text,
                RON real,
                UAH real,
                EUR real,
                USD real,
                GBP real,
                CHF real,
                HUF real,
                AUR real
            )"""
    )
    c.execute(
        """CREATE TABLE deposit (
                date_in text,
                name text,
                owner text,
                sum real,
                currency text,
                months integer,
                date_out text,
                percent real,
                currency_rate real,
                expect real,
                comment text,
                isOpen integer
            )"""
    )
    c.execute(
        """CREATE TABLE transfer (
                id integer,
                date text,
                person_bank_from text,
                person_bank_to text,
                sum real,
                currency text,
                comment text
            )"""
    )
    c.execute(
        """CREATE TABLE advtransfer (
                id integer,
                date text,
                person_bank_from text,
                sum_from real,
                currency_from text,
                person_bank_to text,
                sum_to real,
                currency_to text,
                currency_rate real,
                comment text
            )"""
    )
    c.execute(
        """CREATE TABLE Init_PB (
                person_bank text,
                sum real,
                currency text
            )"""
    )
    c.execute(
        """CREATE TABLE Marker_owner (
                bank_rec text,
                owner text
            )"""
    )
    c.execute(
        """CREATE TABLE Marker_type (
                bank_rec text,
                type text
            )"""
    )
    conn.commit()
    conn.close()


def read_csv(file_name):
    values = []
    with open(file_name, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                values.append(row[0])
    return values


def Add(input_field, mode):
    # Function for adding main, transfer, advtransfer, deposit records and currency rates
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    if mode == "main":
        values = input_field.split(",")
        values[4] = round(float(values[4]), 2)

        c.execute(
            "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
            (values[3], values[5]),
        )  # Check if person_bank - currency pair exists
        exists = c.fetchone()
        if exists == None:
            raise Exception("Person_bank-currency pair does not exist!")

        c.execute("SELECT MAX(id) FROM main")
        max_id = c.fetchone()
        max_id = max_id[0]
        if max_id == None:  # Check if it exist and change to 0 if not
            max_id = 0
        max_id = (
            max_id + 1
        )  # Change so that inserted number is +1 from biggest existing id in DB
        values.insert(0, max_id)

        records = {
            keys[i]: values[i] for i in range(len(keys))
        }  # Make dictionary with all values to add

        c.execute(
            "INSERT INTO main VALUES (:id, :date, :category, :sub_category, :person_bank, :sum, :currency, :comment)",
            records,
        )

    elif mode == "transfer":
        values = input_field.split(",")
        values[3] = round(float(values[3]), 2)
        if values[3] < 0:  # Make sum positive if not
            values[3] = values[3] * -1
        c.execute(
            "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
            (values[2], values[4]),
        )
        # Check if person_bank - currency pair exists
        exists = c.fetchone()
        if exists == None:
            raise Exception("Person_bank-currency pair does not exist!")

        c.execute("SELECT MAX(id) FROM transfer")
        max_id = c.fetchone()
        max_id = max_id[0]
        if max_id == None:  # Check if it is exist and change to 0 if not
            max_id = 0
        max_id = (
            max_id + 1
        )  # Change so that inserted number is +1 from biggest existing id in DB
        values.insert(0, max_id)

        records = {
            tr_keys[i]: values[i] for i in range(len(tr_keys))
        }  # Make dictionary with all values to add

        c.execute(
            "INSERT INTO transfer VALUES (:id, :date, :person_bank_from, :person_bank_to, :sum, :currency, :comment)",
            records,
        )

    elif mode == "advtransfer":
        values = input_field.split(",")
        values[2] = round(float(values[2]), 2)
        values[5] = round(float(values[5]), 2)

        if values[2] < 0:  # Make sum positive if not
            values[2] = values[2] * -1
        if values[5] < 0:
            values[5] = values[5] * -1

        c.execute(
            "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
            (values[1], values[3]),
        )  # Check if sending person_bank - currency pair exists
        exists = c.fetchone()
        if exists == None:
            raise Exception("Person_bank-currency pair does not exist!")

        c.execute(
            "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
            (values[4], values[6]),
        )  # Check if receiving person_bank - currency pair exists
        exists = c.fetchone()
        if exists == None:
            raise Exception("Person_bank-currency pair does not exist!")

        c.execute("SELECT MAX(id) FROM advtransfer")
        max_id = c.fetchone()
        max_id = max_id[0]
        if max_id == None:  # Check if it is exist and change to 0 if not
            max_id = 0
        max_id = (
            max_id + 1
        )  # Change so that inserted number is +1 from biggest existing id in DB
        values.insert(0, max_id)

        records = {
            advtr_keys[i]: values[i] for i in range(len(advtr_keys))
        }  # Make dictionary with all values to add

        c.execute(
            "INSERT INTO advtransfer VALUES (:id, :date, :person_bank_from, :sum_from, :currency_from, :person_bank_to, :sum_to, :currency_to, :currency_rate, :comment)",
            records,
        )

    elif mode == "deposit":
        values = input_field.split(",")

        c.execute(
            "SELECT 1 FROM deposit WHERE name = ?", (values[1],)
        )  # Check if name already exists
        exists = c.fetchone()
        if exists != None:
            raise Exception("Deposit name already exists!")

        c.execute(
            "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
            (values[2], values[4]),
        )  # Check if sending person_bank - currency pair exists
        exists = c.fetchone()
        if exists == None:
            raise Exception("Person_bank-currency pair does not exist!")
        values[3] = round(float(values[3]), 2)
        if values[5] == " ":
            values[5] = 0
        else:
            values[5] = int(values[5])
        values[7] = float(values[7])
        if values[8] == " ":
            values[8] = 0
        else:
            values[8] = float(values[8])

        if values[5] == 0 or values[6] == " ":
            values.insert(9, 0)
        else:
            # Provided formula to calculate deposit return
            percent = values[7] / 100
            expSum = values[3] + (values[3] * (percent / 12) * values[5])
            values.insert(9, round(expSum, 2))
            values.insert(11, 1)

        records = {
            dp_keys[i]: values[i] for i in range(len(dp_keys))
        }  # Make dictionary with all values to add

        c.execute(
            "INSERT INTO deposit VALUES (:date_in, :name, :owner, :sum, :currency, :months, :date_out, :percent, :currency_rate, :expect, :comment, :isOpen)",
            records,
        )

        # Automatically mark deposit as type 'deposit'
        c.execute("INSERT INTO Marker_type VALUES(?, ?)", (values[1], "deposit"))

    elif mode == "currrate":
        values = input_field.split(",")
        for n in range(1, 7):
            values[n] = round(float(values[n]), 4)

        values.insert(2, round(1 / values[1], 2))  # UAH = 1 / RON

        records = {
            curr_keys[i]: values[i] for i in range(len(curr_keys))
        }  # Make dictionary with all values to add

        c.execute(
            "INSERT INTO exc_rate VALUES (:date, :RON, :UAH, :EUR, :USD, :GBP, :CHF, :HUF, :AUR)",
            records,
        )

    conn.commit()
    conn.close()

    Re_Calculate_deposit()


def UpdateRecord(inp):
    # Update record with received input
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    inp = inp.split(",")
    c.execute(
        "UPDATE main SET date = ?, category = ?, sub_category = ?, person_bank = ?, sum = ?, currency = ?, comment = ? WHERE id = ?",
        (inp[1], inp[2], inp[3], inp[4], inp[5], inp[6], inp[7], int(inp[0])),
    )

    conn.commit()
    conn.close()


def Read(x):
    # Big collection of functions for returning different data from DB
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d")

    if x == "allm":
        c.execute("SELECT * FROM main")
        return c.fetchall()
    elif x == "m+":
        c.execute(
            "SELECT id, date, category, person_bank, sum, currency, comment FROM main WHERE sum > 0 ORDER BY date DESC, id DESC"
        )
        return c.fetchall()
    elif x == "m-":
        c.execute("SELECT * FROM main WHERE sum < 0 ORDER BY date DESC, id DESC")
        return c.fetchall()
    elif x == "initpb":
        c.execute("SELECT * FROM Init_PB ORDER BY person_bank DESC")
        return c.fetchall()
    elif x == "allacc":
        c.execute(
            """
                SELECT person_bank, currency, SUM(sum) 
                FROM (
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
                    SELECT person_bank_to AS person_bank, currency, sum FROM transfer) 
                    GROUP BY person_bank, currency
                    ORDER BY person_bank ASC
            """
        )
        return c.fetchall()
    elif x == "alldep":
        c.execute("SELECT * FROM deposit ORDER BY date_out DESC")
        return c.fetchall()
    elif x == "opendep":
        c.execute(
            "SELECT date_in, name, owner, sum, currency, months, date_out, percent, currency_rate, expect, comment FROM deposit WHERE isOpen = 1 ORDER BY date_out DESC"
        )
        return c.fetchall()
    elif x == "closeddep":
        c.execute(
            "SELECT date_in, name, owner, sum, currency, months, date_out, percent, currency_rate, expect, comment FROM deposit WHERE isOpen = 0 ORDER BY date_out DESC"
        )
        return c.fetchall()
    elif x == "alltran":
        c.execute("SELECT * FROM transfer ORDER BY date DESC")
        return c.fetchall()
    elif x == "alladvtran":
        c.execute("SELECT * FROM advtransfer ORDER BY date DESC")
        return c.fetchall()
    elif x == "allcurr":
        c.execute(
            """
                SELECT currency, ROUND(SUM(total_sum), 2) AS total_amount
                FROM (
                    SELECT currency, sum AS total_sum FROM Init_PB
                    
                    UNION ALL
                    
                    SELECT currency, sum AS total_sum FROM main
    
                    UNION ALL
    
                    SELECT currency_from AS currency, -sum_from AS total_sum FROM advtransfer
    
                    UNION ALL
    
                    SELECT currency_to AS currency, sum_to AS total_sum FROM advtransfer
                ) AS combined
                GROUP BY currency    
            """
        )
        return c.fetchall()
    elif x == "allcurrrate":
        c.execute("SELECT * FROM exc_rate ORDER BY date DESC")
        return c.fetchall()

    elif x == "allmtype":
        c.execute(
            """
                SELECT 
                    m.type,
                    ROUND(COALESCE(SUM(normal_account_balances.normal_balance), 0) - COALESCE(SUM(deposit_account_balances.deposit_balance), 0), 2) AS total_balance,
                    COALESCE(normal_account_balances.currency, deposit_account_balances.currency) AS currency
                FROM 
                    Marker_type m
                LEFT JOIN (
                    WITH all_transactions AS (
                    SELECT
                        init.person_bank,
                        currency,
                        SUM(sum) AS normal_balance
                    FROM
                        Init_PB AS init
                    GROUP BY
                        init.person_bank, currency

                    UNION ALL

                    SELECT
                        mt.person_bank,
                        currency,
                        SUM(sum) AS normal_balance
                    FROM
                        main AS mt
                    GROUP BY
                        mt.person_bank, currency

                    UNION ALL

                    SELECT
                        tr.person_bank_from AS person_bank,
                        currency,
                        -SUM(tr.sum) AS normal_balance
                    FROM
                        transfer AS tr
                    GROUP BY
                        tr.person_bank_from, currency

                    UNION ALL

                    SELECT
                        tr.person_bank_to AS person_bank,
                        currency,
                        SUM(tr.sum) AS normal_balance
                    FROM
                        transfer AS tr
                    GROUP BY
                        tr.person_bank_to, currency

                    UNION ALL

                    SELECT
                        at.person_bank_from AS person_bank,
                        currency_from AS currency,
                        -SUM(at.sum_from) AS normal_balance
                    FROM
                        advtransfer AS at
                    GROUP BY
                        at.person_bank_from, currency_from

                    UNION ALL

                    SELECT
                        at.person_bank_to AS person_bank,
                        currency_to AS currency,
                        SUM(at.sum_to) AS normal_balance
                    FROM
                        advtransfer AS at
                    GROUP BY
                        at.person_bank_to, currency_to

                    UNION ALL

                    SELECT    
                        dt.owner AS person_bank,
                        currency,
                        -SUM(dt.sum) AS normal_balance
                    FROM
                        deposit AS dt
                    WHERE
                        dt.isOpen = 1
                    GROUP BY 
                        dt.owner, currency
                )
                SELECT
                    person_bank,
                    currency,
                    SUM(normal_balance) AS normal_balance
                FROM
                    all_transactions
                GROUP BY
                    person_bank, currency
                ) AS normal_account_balances ON m.bank_rec = normal_account_balances.person_bank
                LEFT JOIN (
                    -- Deposit balances
                    SELECT
                        dt.name AS owner,
                        currency,
                        -SUM(dt.sum) AS deposit_balance
                    FROM
                        deposit AS dt
					WHERE
						isOpen = 1
                    GROUP BY
                        dt.name, currency
                ) AS deposit_account_balances ON m.bank_rec = deposit_account_balances.owner
                GROUP BY 
                    m.type, 
                    COALESCE(normal_account_balances.currency, deposit_account_balances.currency)
                """
        )
        return c.fetchall()
    elif x == "allmowner":
        c.execute(
            """
                SELECT 
                    m.owner,
                    ROUND(COALESCE(SUM(all_normal_balances.normal_balance), 0) + COALESCE(SUM(all_normal_balances.deposit_balance), 0), 2) AS total_balance,
                    all_normal_balances.currency AS currency
                FROM 
                    Marker_owner m
                LEFT JOIN (
                    SELECT
                        person_bank,
                        currency,
                        SUM(normal_balance) AS normal_balance,
                        SUM(deposit_balance) AS deposit_balance
                    FROM (
                        SELECT
                            init.person_bank,
                            currency,
                            SUM(sum) AS normal_balance,
                            0 AS deposit_balance
                        FROM
                            Init_PB AS init
                        GROUP BY
                            init.person_bank, currency

                        UNION ALL

                        SELECT
                            mt.person_bank,
                            currency,
                            SUM(sum) AS normal_balance,
                            0 AS deposit_balance
                        FROM
                            main AS mt
                        GROUP BY
                            mt.person_bank, currency

                        UNION ALL

                        SELECT
                            tr.person_bank_from AS person_bank,
                            currency,
                            -SUM(tr.sum) AS normal_balance,
                            0 AS deposit_balance
                        FROM
                            transfer AS tr
                        GROUP BY
                            tr.person_bank_from, currency

                        UNION ALL

                        SELECT
                            tr.person_bank_to AS person_bank,
                            currency,
                            SUM(tr.sum) AS normal_balance,
                            0 AS deposit_balance
                        FROM
                            transfer AS tr
                        GROUP BY
                            tr.person_bank_to, currency

                        UNION ALL

                        SELECT
                            at.person_bank_from AS person_bank,
                            currency_from AS currency,
                            -SUM(at.sum_from) AS normal_balance,
                            0 AS deposit_balance
                        FROM
                            advtransfer AS at
                        GROUP BY
                            at.person_bank_from, currency_from

                        UNION ALL

                        SELECT
                            at.person_bank_to AS person_bank,
                            currency_to AS currency,
                            SUM(at.sum_to) AS normal_balance,
                            0 AS deposit_balance
                        FROM
                            advtransfer AS at
                        GROUP BY
                            at.person_bank_to, currency_to
                    ) AS all_normal_balances
                    GROUP BY person_bank, currency
                ) AS all_normal_balances ON m.bank_rec = all_normal_balances.person_bank
                GROUP BY 
                    m.owner, 
                    all_normal_balances.currency
            """
        )
        return c.fetchall()

    elif x == "extype":
        c.execute("SELECT DISTINCT type FROM Marker_type")
        return c.fetchall()
    elif x == "exowner":
        c.execute("SELECT DISTINCT owner FROM Marker_owner")
        return c.fetchall()
    elif x == "mtype":
        c.execute("SELECT * FROM Marker_type")
        return c.fetchall()
    elif x == "mowner":
        c.execute("SELECT * FROM Marker_owner")
        return c.fetchall()

    elif x == "yeartotalrep":
        c.execute(
            """
            SELECT 
                strftime('%Y-%m', date) AS month, 
                date, 
                sum,
                currency
            FROM main
            ORDER BY month
            """
        )

        result = []
        rows = c.fetchall()

        monthly_data = {}

        for row in rows:
            month = row[0]  # month in 'YYYY-MM' format
            date = row[1]  # transaction date
            amount = row[2]  # amount of the transaction
            currency = row[3]  # currency of the transaction

            # Convert the amount to RON
            amount_in_ron = ConvertToRON(currency, amount, date, c)

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
                round(data["expense"], 2),  # expense in RON
                round(data["income"], 2),  # income in RON
                round(data["total"], 2),  # total in RON
            )
            result.append(month_tuple)

        return result

    elif x == "yearexprep":
        # Fetching the monthly data with expenses per currency
        c.execute(
            """
            SELECT 
                strftime('%Y-%m', "date") AS month,
                currency,
                ROUND(SUM(CASE WHEN sum < 0 THEN ABS(sum) ELSE 0 END), 2) AS total_expense,
                "date"
            FROM main
            WHERE sum < 0
            GROUP BY month, currency
            ORDER BY month
            """
        )

        result = []
        rows = c.fetchall()
        currencies = read_csv(SPVcurrPath)
        monthly_data = {}

        for row in rows:
            month = row[0]
            currency = row[1]
            total = row[2]
            date = row[3]

            # Initialize the monthly data with currency totals if not already present
            if month not in monthly_data:
                monthly_data[month] = {curr: 0 for curr in currencies}
                monthly_data[month][
                    "total_in_RON"
                ] = 0  # Initialize RON total for the month

            # If currency is found in the list of valid currencies
            if currency in currencies:
                monthly_data[month][currency] = total

                # Convert the total to RON using the conversion function
                total_in_RON = ConvertToRON(currency, total, date, c)
                monthly_data[month]["total_in_RON"] += total_in_RON

        # Prepare the result for each month with the total per currency and total in RON
        for month in sorted(monthly_data.keys()):
            month_tuple = (
            (month,)
            + tuple(round(monthly_data[month][currency], 2) for currency in currencies)
            + (round(monthly_data[month]["total_in_RON"], 2),)
            )  # Append RON total
            result.append(month_tuple)

        return result

    elif x == "yearincrep":
        c.execute(
            """
            SELECT 
                strftime('%Y-%m', "date") AS month,
                currency,
                ROUND(SUM(CASE WHEN sum > 0 THEN ABS(sum) ELSE 0 END), 2) AS total_income,
                "date"
            FROM main
            WHERE sum > 0
            GROUP BY month, currency
            ORDER BY month
            """
        )

        result = []
        rows = c.fetchall()
        currencies = read_csv(SPVcurrPath)
        monthly_data = {}

        for row in rows:
            month = row[0]
            currency = row[1]
            total = row[2]
            date = row[3]

            # Initialize the monthly data with currency totals if not already present
            if month not in monthly_data:
                monthly_data[month] = {curr: 0 for curr in currencies}
                monthly_data[month][
                    "total_in_RON"
                ] = 0  # Initialize RON total for the month

            # If currency is found in the list of valid currencies
            if currency in currencies:
                monthly_data[month][currency] = total

                # Convert the total to RON using the conversion function
                total_in_RON = ConvertToRON(currency, total, date, c)
                monthly_data[month]["total_in_RON"] += total_in_RON

        # Prepare the result for each month with the total per currency and total in RON
        for month in sorted(monthly_data.keys()):
            month_tuple = (
                (month,)
                + tuple(round(monthly_data[month][currency], 2) for currency in currencies)
                + (round(monthly_data[month]["total_in_RON"], 2),)
            )  # Append RON total
            result.append(month_tuple)

        return result

    elif x == "retacc":  # Return list of all accounts
        c.execute("SELECT DISTINCT person_bank FROM Init_PB ORDER BY person_bank ASC")
        result = [row[0] for row in c.fetchall()]
        return result

    elif x == "retmowner":  # Return list of all owners
        c.execute("SELECT DISTINCT owner FROM Marker_owner")
        result = [row[0] for row in c.fetchall()]
        return result

    elif x == "retmtype":  # Return list of all types
        c.execute("SELECT DISTINCT type FROM Marker_type")
        result = [row[0] for row in c.fetchall()]
        return result

    elif x == "retcurrr":
        query = "SELECT Date, RON, EUR, USD, GBP, CHF FROM exc_rate ORDER BY date"
        df = pd.read_sql_query(query, conn)
        return df

    elif x == "retcurraur":
        query = "SELECT Date, AUR FROM exc_rate ORDER BY date"
        df = pd.read_sql_query(query, conn)
        return df

    conn.commit()
    conn.close()


def read_and_convert_data(x, mode, cursor):
    current_date = datetime.now().strftime("%Y-%m-%d")

    if x == "norm":
        data = Read(mode)
    else:
        data = MarkerRead(x, mode)
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

            converted_amount = ConvertToRON(currency_column, amount, current_date, cursor)

            if owner in modified_dict:
                modified_dict[owner] += converted_amount
            else:
                modified_dict[owner] = converted_amount

    return modified_dict

def ConvRead(x, mode, include_percentage=False):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    modified_dict = read_and_convert_data(x, mode, c)

    # Calculate the total sum of all amounts
    total_sum = sum(modified_dict.values())

    # Convert the grouped data back into a list of tuples
    if include_percentage:
        modified_list = [
            (owner, round(total_amount, 2), round((total_amount / total_sum) * 100, 2))
            for owner, total_amount in modified_dict.items()
        ]
    else:
        modified_list = [
            (owner, round(total_amount, 2))
            for owner, total_amount in modified_dict.items()
        ]

    conn.commit()
    conn.close()

    return modified_list


def ConvReadPlus(x, mode):
    # Function for reading DB and returning converted to RON amounts
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")

    if x == "norm":
        data = Read(mode)
    else:
        data = MarkerRead(x, mode)
    modified_list = []

    for row in data:
        row_list = list(row)
        owner = row_list[0]
        amount = round(row_list[1], 2)
        currency_column = row_list[2]

        converted_amount = ConvertToRON(currency_column, amount, current_date, c)

        # Append the tuple with the converted amount
        modified_list.append((owner, currency_column, amount, converted_amount))

    conn.commit()
    conn.close()

    return modified_list


def ReadAdv(type, month):
    # Special read function for reports with month selector
    conn = sqlite3.connect(dbPath)
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
        categories_df = pd.read_csv(SPVcatIncPath, header=None)
        categories_list = categories_df[0].tolist()

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
            category = row[0]
            currency = row[1]
            amount = row[2]
            date = row[3]

            converted_amount = ConvertToRON(currency, amount, date, c)

            if category in modified_dict:
                modified_dict[category] += converted_amount
            else:
                modified_dict[category] = converted_amount

        total_income = sum(modified_dict.values())

        # Convert the grouped data back into a list of tuples with percentage
        modified_list = [
            (category, round(total_amount, 2), round((total_amount / total_income) * 100, 2)) 
            for category, total_amount in modified_dict.items()
        ]

        conn.commit()
        conn.close()

        return modified_list

    elif type == "catexprep":
        categories_df = pd.read_csv(SPVcatExpPath, header=None)
        categories_list = categories_df[0].tolist()

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
            (category, round(total_amount, 2), f"{(total_amount / total_expense) * 100:.0f}%")
            for category, total_amount in modified_dict.items()
        ]

        conn.commit()
        conn.close()

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


def ConvertToRON(currency, amount, date, c):
    # Converting to RON

    if currency != "RON":
        query = f"SELECT {currency} FROM exc_rate ORDER BY ABS(JULIANDAY(date) - JULIANDAY('{date}')) LIMIT 1"
        c.execute(query)
        excRate_row = c.fetchone()
        if excRate_row != None:
            excRate = excRate_row[0]  # Extract the exchange rate
        else:
            excRate = 1
    else:
        excRate = 1
    converted_amount = round(amount * excRate, 2)

    return converted_amount


def MarkerRead(markers, mode):
    # Function for returning markers sums for type/owner/both markers
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    person_banks = []

    if mode == "byowner":
        c.execute(
            """
                SELECT
                    bank_rec
                FROM
                    Marker_owner
                WHERE
                    owner = ?
                """,
            (markers,),
        )
        person_banks = c.fetchall()

    elif mode == "bytype":
        c.execute(
            """
                SELECT
                    bank_rec
                FROM
                    Marker_type
                WHERE
                    type = ?
                """,
            (markers,),
        )
        person_banks = c.fetchall()

    elif mode == "byall":
        values = markers.split(",")
        c.execute(
            """
                SELECT
                    mo.bank_rec
                FROM
                    Marker_owner mo
                JOIN
                    Marker_type mt ON mo.bank_rec = mt.bank_rec
                WHERE
                    mo.owner = ?
                    AND
                    mt.type = ?                   
                """,
            (values[0], values[1]),
        )
        person_banks = c.fetchall()

    if person_banks:
        person_banks = [pb[0] for pb in person_banks]
        # Prepare dynamic query to calculate balances using person_banks
        seq = ",".join(["?"] * len(person_banks))

        # This query combines the balances from multiple sources and also integrates PBD logic
        c.execute(
            f"""
                SELECT person_bank, currency, ROUND(SUM(sum), 2) AS sum
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
                )
                WHERE person_bank IN ({seq})
                GROUP BY person_bank, currency
                """,
            person_banks,
        )

        results = c.fetchall()
        conn.commit()
        conn.close()

        return results
    else:
        conn.commit()
        conn.close()
        return []


def Del(del_id, type):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    if type == "main":
        c.execute("SELECT 1 FROM main WHERE id = ?", (del_id,))
        exists = c.fetchone()
        if exists != None:
            c.execute("DELETE FROM main WHERE id = ?", (del_id,))
        else:
            print("Record with id ", del_id, " does not exist.\n")

    elif type == "transfer":
        c.execute("SELECT 1 FROM transfer WHERE id = ?", (del_id,))
        exists = c.fetchone()
        if exists != None:
            c.execute("DELETE FROM transfer WHERE id = ?", (del_id,))
        else:
            print("Record with id ", del_id, " does not exist.\n")

    conn.commit()
    conn.close()


def Re_Calculate_deposit():
    # Function for calculating if deposit is due or not
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    # Check active deposits and create income/expense if due
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Fetch active deposits from the deposit table where sum != 0 and the deposit is not expired
    c.execute(
        """
        SELECT name
        FROM deposit 
        WHERE isOpen = 1 AND (date_out <= ? OR date_out = ' ')
        """,
        (current_date,)
    )
    open_deposits = c.fetchall()

    for deposit in open_deposits:
        name = deposit[0]

        # Mark the deposit as fully processed (sum = 0)
        c.execute(
            """
            UPDATE deposit 
            SET isOpen = 0
            WHERE name = ?
            """,
            (name,)
        )
        c.execute(
            """
                DELETE
                FROM 
                    Marker_type
                WHERE bank_rec = ?
                  """,
            (name,)
        )

    conn.commit()
    conn.close()


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


def ShowExistingSPVAPI(x):
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
            output = io.StringIO()
            output.write("Existing values:\n")
            for lines in csvFile:
                output.write(", ".join(lines) + "\n")
            return output.getvalue()
    else:
        return "File does not exist."


def InitPB(new_pb):
    # Person_bank initialization function
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    new_pb = new_pb.split(",")

    c.execute(
        "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
        (new_pb[0], new_pb[2]),
    )
    exists = c.fetchone()
    if exists != None:
        print("Record already exists!\n\n")
        return
    else:
        c.execute(
            "INSERT INTO Init_PB (person_bank, sum, currency) VALUES (?, ?, ?)",
            (new_pb[0], new_pb[1], new_pb[2]),
        )
        print("Success!\n\n")

    conn.commit()
    conn.close()


def Mark(marker, mode):
    # Function pushing special record into DB with marker: whose or what type of account is this
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    marker = marker.split(",")
    c.execute(
        "SELECT 1 FROM (Init_PB pb, deposit pbd) WHERE pb.person_bank = ? OR pbd.name = ?",
        (marker[0], marker[0]),
    )
    exists = c.fetchone()
    if exists != None:
        print("Account record does not exist!\n\n")
        return

    if mode == "type":
        c.execute("SELECT 1 FROM Marker_type WHERE bank_rec = ?", (marker[0],))
        exists = c.fetchone()
        if exists != None:
            c.execute(
                "UPDATE Marker_type SET bank_rec = ?, type = ? WHERE bank_rec = ?",
                (marker[0], marker[1], marker[0]),
            )
        else:
            c.execute(
                "INSERT INTO Marker_type (bank_rec, type) VALUES (?, ?)",
                (marker[0], marker[1]),
            )
            print("Success!\n\n")

    elif mode == "owner":
        c.execute("SELECT 1 FROM Marker_owner WHERE bank_rec = ?", (marker[0],))
        exists = c.fetchone()
        if exists != None:
            c.execute(
                "UPDATE Marker_owner SET bank_rec = ?, owner = ? WHERE bank_rec = ?",
                (marker[0], marker[1], marker[0]),
            )
        else:
            c.execute(
                "INSERT INTO Marker_owner (bank_rec, owner) VALUES (?, ?)",
                (marker[0], marker[1]),
            )
            print("Success!\n\n")

    conn.commit()
    conn.close()


def DelPB(pb):
    # Delete person_bank
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    pb = pb.split(",")
    try:
        c.execute(
            "DELETE FROM Init_PB WHERE person_bank = ? AND currency = ?", (pb[0], pb[1])
        )
        c.execute(
            "DELETE FROM main WHERE person_bank = ? AND currency = ?", (pb[0], pb[1])
        )
        c.execute(
            "DELETE FROM transfer WHERE person_bank_from = ? AND currency = ?",
            (pb[0], pb[1]),
        )
        c.execute(
            "DELETE FROM transfer WHERE person_bank_to = ? AND currency = ?",
            (pb[0], pb[1]),
        )
        c.execute(
            "DELETE FROM advtransfer WHERE person_bank_from = ? AND currency_from = ?",
            (pb[0], pb[1]),
        )
        c.execute(
            "DELETE FROM advtransfer WHERE person_bank_to = ? AND currency_to = ?",
            (pb[0], pb[1]),
        )
        c.execute(
            "DELETE FROM deposit WHERE person_bank = ? AND currency = ?", (pb[0], pb[1])
        )
        c.execute("DELETE FROM Marker_type WHERE banc_rec = ?", (pb[0],))
        c.execute("DELETE FROM Marker_owner WHERE banc_rec = ?", (pb[0],))
    except:
        print("Failure!\n\n")
    print("Success!\n\n")

    conn.commit()
    conn.close()

    Re_Calculate_deposit()


def GrabRecordByID(id, mode):
    # Function for getting record by ID. Used for editing/updating
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    if mode == "exp":
        c.execute("SELECT * FROM main WHERE id = ?", (id,))
        record = c.fetchall()

    elif mode == "inc":
        c.execute(
            "SELECT id, date, category, person_bank, sum, currency, comment FROM main WHERE id = ?",
            (id,),
        )
        record = c.fetchall()

    conn.commit()
    conn.close()

    return record
