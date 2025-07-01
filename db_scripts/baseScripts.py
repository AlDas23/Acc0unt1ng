from datetime import datetime
import os.path
import sqlite3
import pandas as pd
from db_scripts.consts import *
from db_scripts.csvScripts import read_csv


def NewDBase():
    # Create or replace DB file using template
    directory = os.path.dirname(dbPath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(dbPath):
        os.remove(dbPath)

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        c.execute(
            """CREATE TABLE main (
                    id integer PRIMARY KEY,
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
                    HUF real
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
        # Invest tables
        c.execute(
            """CREATE TABLE investTransaction (
                    id integer PRIMARY KEY,
                    date text,
                    PB text,
                    amount real,
                    currency text,
                    investPB text,
                    investAmount real,
                    stock text, 
                    fee real
                )"""
        )
        c.execute(
            """CREATE TABLE investPB (
                    name text,
                    stock text
                )"""
        )
        c.execute(
            """CREATE TABLE investStockPrice (
                    id integer PRIMARY KEY,
                    date text,
                    stock text,
                    price real
                )"""
        )

        conn.commit()


def Add(input_field, mode):
    # Function for adding main, transfer, advtransfer, deposit records and currency rates
    with sqlite3.connect(dbPath) as conn:
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

            records = {
                keys[i]: values[i] for i in range(len(keys))
            }  # Make dictionary with all values to add

            c.execute(
                "INSERT INTO main VALUES (NULL, :date, :category, :sub_category, :person_bank, :sum, :currency, :comment)",
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
            for n in range(1, 6):
                values[n] = round(
                    float(values[n] if values[n].strip() != " " else 0), 4
                )

            values.insert(2, round(1 / values[1], 4))  # UAH = 1 / RON

            records = {
                curr_keys[i]: values[i] for i in range(len(curr_keys))
            }  # Make dictionary with all values to add

            c.execute(
                "INSERT INTO exc_rate VALUES (:date, :RON, :UAH, :EUR, :USD, :GBP, :CHF, :HUF)",
                records,
            )

        conn.commit()

    Re_Calculate_deposit()


def Read(x):
    # Big collection of functions for returning different data from DB
    with sqlite3.connect(dbPath) as conn:
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
        elif x == "yeartotal":
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
            return c.fetchall()

        elif x == "yearexp":
            c.execute(
                """
                SELECT 
                    strftime('%Y-%m', "date") AS month,
                    currency,
                    ABS(sum) AS expense,
                    "date"
                FROM main
                WHERE sum < 0
                ORDER BY month
                """
            )
            return c.fetchall()

        elif x == "yearinc":
            c.execute(
                """
                    SELECT 
                        strftime('%Y-%m', "date") AS month,
                        currency,
                        ABS(sum) AS income,
                        "date"
                    FROM main
                    WHERE sum > 0
                    GROUP BY month, currency
                    ORDER BY month
                    """
            )
            return c.fetchall()

        elif x == "retacc":  # Return list of all accounts
            c.execute(
                "SELECT DISTINCT person_bank FROM Init_PB ORDER BY person_bank ASC"
            )
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

        elif x == "retcat":
            c.execute("SELECT DISTINCT category FROM main ORDER BY category DESC")
            result = [row[0] for row in c.fetchall()]
            return result

        elif x == "retcat+":
            c.execute(
                "SELECT DISTINCT category FROM main WHERE sum > 0 ORDER BY category DESC"
            )
            result = [row[0] for row in c.fetchall()]
            return result

        elif x == "retcat-":
            c.execute(
                "SELECT DISTINCT category FROM main WHERE sum < 0 ORDER BY category DESC"
            )
            result = [row[0] for row in c.fetchall()]
            return result


def MarkerRead(mode, markers=None):
    # Function for returning markers sums for type/owner/both markers
    with sqlite3.connect(dbPath) as conn:
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

        elif mode == "none":
            # If no markers are provided, return all person banks
            c.execute("SELECT DISTINCT person_bank FROM Init_PB")
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
            return results
        else:
            return []


def Del(del_id, type):
    with sqlite3.connect(dbPath) as conn:
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


def Re_Calculate_deposit():
    # Function for calculating if deposit is due or not
    with sqlite3.connect(dbPath) as conn:
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
            (current_date,),
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
                (name,),
            )
            c.execute(
                """
                    DELETE
                    FROM 
                        Marker_type
                    WHERE bank_rec = ?
                    """,
                (name,),
            )

        conn.commit()


def InitPB(new_pb):
    # Person_bank initialization function
    with sqlite3.connect(dbPath) as conn:
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


def Mark(marker, mode):
    # Function pushing special record into DB with marker: whose or what type of account is this
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        marker = marker.split(",")
        c.execute(
            "SELECT 1 FROM (Init_PB pb, deposit pbd) WHERE pb.person_bank = ? OR pbd.name = ?",
            (marker[0], marker[0]),
        )
        exists = c.fetchone()
        if exists is None:
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


def DelPB(pb):
    # Delete person_bank
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        pb = pb.split(",")
        try:
            c.execute(
                "DELETE FROM Init_PB WHERE person_bank = ? AND currency = ?",
                (pb[0], pb[1]),
            )
            c.execute(
                "DELETE FROM main WHERE person_bank = ? AND currency = ?",
                (pb[0], pb[1]),
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
                "DELETE FROM deposit WHERE person_bank = ? AND currency = ?",
                (pb[0], pb[1]),
            )
            c.execute("DELETE FROM Marker_type WHERE banc_rec = ?", (pb[0],))
            c.execute("DELETE FROM Marker_owner WHERE banc_rec = ?", (pb[0],))
        except:
            print("Failure!\n\n")
        print("Success!\n\n")

        conn.commit()

    Re_Calculate_deposit()


def GrabRecordByID(id, mode):
    # Function for getting record by ID. Used for editing/updating
    with sqlite3.connect(dbPath) as conn:
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

    return record
