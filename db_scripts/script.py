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
                comment text
            )"""
    )
    c.execute(
        """CREATE TABLE PB_account_deposit (
                name text,
                person_bank text,
                sum real,
                currency text
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
        """CREATE TABLE PB_account (
                person_bank text,
                sum real,
                currency text
            )"""
    )
    c.execute(
        """CREATE TABLE Marker_owner (
                person_bank text,
                owner text
            )"""
    )
    c.execute(
        """CREATE TABLE Marker_type (
                person_bank text,
                type text
            )"""
    )
    conn.commit()
    conn.close()


def Add(input_field, mode):
    # Function for adding main, transfer, advtransfer, deposit records and currency rates
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    if mode == "main":
        values = input_field.split(",")
        values[4] = round(float(values[4]), 2)
        c.execute(
            "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ?",
            (values[3], values[5]),
        )  # Check if person_bank - currency pair exists
        exists = c.fetchone()
        if exists == None:
            raise Exception("Person_bank-currency pair does not exist!")
        if values[4] < 0:
            c.execute(
                "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ? AND sum > ?",
                (values[3], values[5], values[4]),
            )  # Check if person_bank - currency pair has enough amount
            exists = c.fetchone()
            if exists == None:
                raise Exception("Insufficient funds!")

        c.execute("SELECT MAX(id) FROM main")
        max_id = c.fetchone()
        max_id = max_id[0]
        if max_id == None:  # Check if it is exist and change to 0 if not
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
            "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ? AND sum > ?",
            (values[2], values[4], values[3]),
        )  # Check if person_bank - currency pair exists and has sufficient amount
        exists = c.fetchone()
        if exists == None:
            raise Exception(
                "Person_bank-currency pair does not exist or insufficient funds!"
            )

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
            "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ? AND sum >= ?",
            (values[1], values[3], values[2]),
        )  # Check if sending person_bank - currency pair exists and has sufficient amount
        exists = c.fetchone()
        if exists == None:
            raise Exception(
                "Person_bank-currency pair does not exist or insufficient funds!"
            )
        c.execute(
            "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ?",
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
            "INSERT INTO advtransfer VALUES (:id, :date, :person_bank_from, :sum_from, :currency_from, :person_bank_to, :sum_to, :currency_to, :currency_rate :comment)",
            records,
        )

    elif mode == "deposit":
        values = input_field.split(",")
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
            values.insert(10, round(expSum, 2))

        records = {
            dp_keys[i]: values[i] for i in range(len(dp_keys))
        }  # Make dictionary with all values to add

        c.execute(
            "INSERT INTO deposit VALUES (:date_in, :name, :owner, :sum, :currency, :months, :date_out, :percent, :currency_rate, :expect, :comment)",
            records,
        )

        # TODO Automatically mark deposit as type 'deposit'. Now main person_bank is used as deposit core

    elif mode == "currrate":
        values = input_field.split(",")
        for n in range(1, 7):
            values[n] = round(float(values[n]), 2)

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

    Re_calculate()


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

    Re_calculate()


def Read(x):
    # Big collection of functions for returning different data from DB
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

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
    elif x == "allacc":
        c.execute("SELECT * FROM PB_account ORDER BY person_bank ASC")
        return c.fetchall()
    elif x == "alldepacc":
        c.execute(
            "SELECT * FROM PB_account_deposit WHERE sum != 0 ORDER BY person_bank ASC"
        )
        return c.fetchall()
    elif x == "alldep":
        c.execute("SELECT * FROM deposit ORDER BY date_out DESC")
        return c.fetchall()
    elif x == "opendep":
        current_date = datetime.now().strftime("%Y-%m-%d")
        c.execute(
            "SELECT * FROM deposit WHERE date_out > ? OR date_out == ' ' ORDER BY date_out DESC",
            (current_date,),
        )
        return c.fetchall()
    elif x == "closeddep":
        current_date = datetime.now().strftime("%Y-%m-%d")
        c.execute(
            "SELECT * FROM deposit WHERE date_out <= ? AND date_out != ' ' ORDER BY date_out DESC",
            (current_date,),
        )
        return c.fetchall()
    elif x == "alltran":
        c.execute("SELECT * FROM transfer ORDER BY date DESC")
        return c.fetchall()
    elif x == "alladvtran":
        c.execute("SELECT * FROM advtransfer ORDER BY date DESC")
        return c.fetchall()
    elif x == "allcurr":
        c.execute("SELECT currency, SUM(sum) FROM PB_account GROUP BY currency")
        return c.fetchall()
    elif x == "allcurrrate":
        c.execute("SELECT * FROM exc_rate ORDER BY date DESC")
        return c.fetchall()

    elif x == "allmtype":
        c.execute(
            """
                SELECT 
                    m.type,
                    COALESCE(SUM(pb.sum), 0) + COALESCE(SUM(pbd.sum), 0) as total_balance,
                    pb.currency as pb_currency
                FROM 
                    Marker_type m
                LEFT JOIN PB_account pb ON m.person_bank = pb.person_bank
                LEFT JOIN PB_account_deposit pbd ON m.person_bank = pbd.person_bank
                GROUP BY 
                    m.type, 
                    pb.currency
                """
        )
        return c.fetchall()
    elif x == "allmowner":
        c.execute(
            """
                SELECT 
                    m.owner,
                    COALESCE(SUM(pb.sum), 0) + COALESCE(SUM(pbd.sum), 0) as total_balance,
                    pb.currency as pb_currency
                FROM 
                    Marker_owner m
                LEFT JOIN PB_account pb ON m.person_bank = pb.person_bank
                LEFT JOIN PB_account_deposit pbd ON m.person_bank = pbd.person_bank
                GROUP BY 
                    m.owner, 
                    pb.currency
                """
        )
        return c.fetchall()

    elif x == "extype":
        c.execute("SELECT DISTINCT type FROM Marker_type")
        return c.fetchall()
    elif x == "exowner":
        c.execute("SELECT DISTINCT owner FROM Marker_owner")
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
                data["expense"],  # expense in RON
                data["income"],  # income in RON
                data["total"],  # total in RON
            )
            result.append(month_tuple)

        return result

    elif x == "retacc":  # Return list of all accounts
        c.execute("SELECT DISTINCT person_bank FROM PB_account")
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


def ConvRead(x, mode):
    # Function for reading DB and returning converted to RON amounts
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")

    if x == "norm":
        data = Read(mode)
    else:
        data = MarkerRead(x, mode)
    modified_dict = {}

    for row in data:
        row_list = list(row)
        owner = row_list[0]
        amount = row_list[1]
        currency_column = row_list[2]

        converted_amount = ConvertToRON(currency_column, amount, current_date, c)

        if owner in modified_dict:
            modified_dict[owner] += converted_amount
        else:
            modified_dict[owner] = converted_amount

    # Convert the grouped data back into a list of tuples
    modified_list = [
        (owner, total_amount) for owner, total_amount in modified_dict.items()
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
        amount = row_list[1]
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
        modified_list = []

        # Convert to RON using dynamic table
        for row in data:
            category = row[0]
            currency = row[1]
            amount = row[2]
            date = row[3]

            converted_amount = ConvertToRON(currency, amount, date, c)

            # Append the tuple with the converted amount
            modified_list.append((category, currency, amount, converted_amount))

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

        # Calculate the total income in RON
        total_expense = sum(modified_dict.values())

        # Convert the grouped data back into a list of tuples
        modified_list = [
            (category, total_amount, f"{(total_amount / total_expense) * 100:.2f}%")
            for category, total_amount in modified_dict.items()
        ]

        conn.commit()
        conn.close()

        return modified_list

    elif type == "catincbankrep":
        categories_df = pd.read_csv(SPVcatIncPath, header=None)
        categories_list = categories_df[0].tolist()

        query = """
        SELECT category, person_bank, currency, sum
        FROM main
        WHERE category IN ({})
        GRUP BY category, person_bank
        ORDER BY currency DESC
        """.format(
            ",".join("?" for _ in categories_list)
        )

        params = categories_list + [month]
        c.execute(query, params)

        return c.fetchall()


def ConvertToRON(currency, amount, date, c):
    # Converting to RON

    if currency != "RON":
        query = f"SELECT {currency} FROM exc_rate ORDER BY ABS(JULIANDAY(date) - JULIANDAY(?)) LIMIT 1"
        c.execute(query, (date,))
        excRate_row = c.fetchone()
        if excRate_row != None:
            excRate = excRate_row[0]  # Extract the exchange rate
        else:
            excRate = 1
    else:
        excRate = 1
    converted_amount = amount * excRate

    return converted_amount


def MarkerRead(markers, mode):
    # Function for returning markers sums for type/owner/both markers
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    if mode == "byowner":
        c.execute(
            """
                SELECT
                    person_bank
                FROM
                    Marker_owner
                WHERE
                    owner = ?
                """,
            (markers,),
        )
        person_banks = c.fetchall()

        person_banks = [pb[0] for pb in person_banks]
        results = []

        c.execute(
            """
                SELECT
                    person_bank,
                    sum,
                    currency
                FROM
                    PB_account
                WHERE
                    person_bank IN ({seq})
                """.format(
                seq=",".join(["?"] * len(person_banks))
            ),
            person_banks,
        )
        results.extend(c.fetchall())

        c.execute(
            """
                SELECT
                    person_bank,
                    sum,
                    currency
                FROM
                    PB_account_deposit
                WHERE 
                    person_bank IN ({seq})
                """.format(
                seq=",".join(["?"] * len(person_banks))
            ),
            person_banks,
        )
        results.extend(c.fetchall())

        return results

    elif mode == "bytype":
        c.execute(
            """
                SELECT
                    person_bank
                FROM
                    Marker_type
                WHERE
                    type = ?
                """,
            (markers,),
        )
        person_banks = c.fetchall()

        person_banks = [pb[0] for pb in person_banks]
        results = []

        c.execute(
            """
                SELECT
                    person_bank,
                    sum,
                    currency
                FROM
                    PB_account
                WHERE
                    person_bank IN ({seq})
                """.format(
                seq=",".join(["?"] * len(person_banks))
            ),
            person_banks,
        )
        results.extend(c.fetchall())

        c.execute(
            """
                SELECT
                    person_bank,
                    sum,
                    currency
                FROM
                    PB_account_deposit
                WHERE 
                    person_bank IN ({seq})
                """.format(
                seq=",".join(["?"] * len(person_banks))
            ),
            person_banks,
        )
        results.extend(c.fetchall())

        return results

    elif mode == "byall":
        values = markers.split(",")
        c.execute(
            """
                SELECT
                    mo.person_bank
                FROM
                    Marker_owner mo
                JOIN
                    Marker_type mt ON mo.person_bank = mt.person_bank
                WHERE
                    mo.owner = ?
                    AND
                    mt.type = ?                   
                """,
            (values[0], values[1]),
        )
        person_banks = c.fetchall()

        person_banks = [pb[0] for pb in person_banks]
        results = []

        c.execute(
            """
                SELECT
                    person_bank,
                    sum,
                    currency
                FROM
                    PB_account
                WHERE
                    person_bank IN ({seq})
                """.format(
                seq=",".join(["?"] * len(person_banks))
            ),
            person_banks,
        )
        results.extend(c.fetchall())

        c.execute(
            """
                SELECT
                    person_bank,
                    sum,
                    currency
                FROM
                    PB_account_deposit
                WHERE 
                    person_bank IN ({seq})
                """.format(
                seq=",".join(["?"] * len(person_banks))
            ),
            person_banks,
        )
        results.extend(c.fetchall())

        return results

    conn.commit()
    conn.close()


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

    Re_calculate()

    conn.commit()
    conn.close()


def Re_calculate():
    # Core function for calculating remainders on all accounts. Called after each each finished add, update or delete
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    # Calculate sums for each person_bank and currency pair
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
            SELECT person_bank_to AS person_bank, currency, sum FROM transfer
            UNION ALL
            SELECT owner AS person_bank, currency, -sum FROM deposit
        )
        GROUP BY person_bank, currency
    """
    )
    sums = c.fetchall()

    for person_bank, currency, total_sum in sums:
        c.execute(
            "SELECT COUNT(*) FROM PB_account WHERE person_bank = ? AND currency = ?",
            (person_bank, currency),
        )
        row_exists = c.fetchone()[0]

        if row_exists:
            c.execute(
                "UPDATE PB_account SET sum = ? WHERE person_bank = ? AND currency = ?",
                (round(total_sum, 2), person_bank, currency),
            )
        else:
            c.execute(
                "INSERT INTO PB_account (person_bank, sum, currency) VALUES (?, ?, ?)",
                (person_bank, round(total_sum, 2), currency),
            )

    # Calculate deposit sums for each person_bank and currency pair
    c.execute(
        """
        SELECT name, person_bank, currency, SUM(sum) 
        FROM (
                SELECT name, owner AS person_bank, currency, sum FROM deposit
            )
        GROUP BY name, person_bank, currency
    """
    )
    DSums = c.fetchall()

    for name, person_bank, currency, total_sum in DSums:
        c.execute(
            "SELECT COUNT(*) FROM PB_account_deposit WHERE name = ? AND person_bank = ? AND currency = ?",
            (name, person_bank, currency),
        )
        row_exists = c.fetchone()[0]

        if row_exists:
            c.execute(
                "UPDATE PB_account_deposit SET sum = ? WHERE name = ? AND person_bank = ? AND currency = ?",
                (round(total_sum, 2), name, person_bank, currency),
            )
        else:
            c.execute(
                "INSERT INTO PB_account_deposit (name, person_bank, sum, currency) VALUES (?, ?, ?, ?)",
                (name, person_bank, round(total_sum, 2), currency),
            )

    # Check active deposits and create income/expense if due
    c.execute(
        "SELECT name, person_bank, sum, currency FROM PB_account_deposit WHERE sum != 0"
    )
    openD = c.fetchall()
    current_date = datetime.now().strftime("%Y-%m-%d")

    for deposit in openD:
        name, owner, sum, currency = deposit
        c.execute(
            "SELECT name, owner, sum, currency FROM deposit WHERE name = ? AND date_out < ? AND date_out != ' '",
            (name, current_date),
        )
        expired = c.fetchone()

        if expired:
            c.execute(
                "UPDATE PB_account_deposit SET sum = 0 WHERE name = ? AND person_bank = ? AND currency = ?",
                (expired[0], expired[1], expired[3]),
            )

            c.execute("SELECT MAX(id) FROM main")
            max_id = c.fetchone()[0]
            max_id = 0 if max_id is None else max_id + 1

            c.execute(
                """
                INSERT INTO main (
                    id,
                    date,
                    category,
                    sub_category,
                    person_bank,
                    comment,
                    sum,
                    currency
                ) VALUES (?, ?, ' ', ' ', ?, 'Deposit return', ?, ?)
            """,
                (max_id, current_date, expired[1], expired[2], expired[3]),
            )

    conn.commit()
    conn.close()


def SPVconf(pth, new_SPV, inpMode):
    # Function for configuring categories and currencies. TODO remake function to be used in API
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
        "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ?",
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

    Re_calculate()


def Mark(marker, mode):
    # Function pushing special record into DB with marker: whose or what type of account is this
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    marker = marker.split(",")

    c.execute(
        "SELECT 1 FROM (PB_account pb, PB_account_deposit pbd) WHERE pb.person_bank = ? OR pbd.person_bank = ?",
        (marker[0], marker[0]),
    )
    exists = c.fetchone()
    if exists != None:
        print("Person_bank does not exist!\n\n")
        return

    if mode == "type":
        c.execute(
            "SELECT 1 FROM Marker_type WHERE person_bank = ? AND type = ?",
            (marker[0], marker[1]),
        )
        exists = c.fetchone()
        if exists != None:
            c.execute(
                "UPDATE Marker_type SET person_bank = ?, type = ? WHERE person_bank = ?",
                (marker[0], marker[1], marker[0]),
            )
        else:
            c.execute(
                "INSERT INTO Marker_type (person_bank, type) VALUES (?, ?)",
                (marker[0], marker[1]),
            )
            print("Success!\n\n")

    elif mode == "owner":
        c.execute(
            "SELECT 1 FROM Marker_owner WHERE person_bank = ? AND owner = ?",
            (marker[0], marker[1]),
        )
        exists = c.fetchone()
        if exists != None:
            c.execute(
                "UPDATE Marker_owner SET person_bank = ?, owner = ? WHERE person_bank = ?",
                (marker[0], marker[1], marker[0]),
            )
        else:
            c.execute(
                "INSERT INTO Marker_owner (person_bank, owner) VALUES (?, ?)",
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
            "DELETE FROM PB_account WHERE person_bank = ? AND currency = ?",
            (pb[0], pb[1]),
        )
        c.execute(
            "DELETE FROM Init_PB WHERE person_bank = ? AND currency = ?", (pb[0], pb[1])
        )
    except:
        print("Failure!\n\n")
    print("Success!\n\n")

    conn.commit()
    conn.close()

    Re_calculate()


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
