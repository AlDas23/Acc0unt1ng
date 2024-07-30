import os.path
import csv
import sqlite3
import pandas as pd
from datetime import datetime
from db_scripts.consts import *


def NewDBase():
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
        """CREATE TABLE deposit (
                date_in text,
                name text,
                owner text,
                sum real,
                currency text,
                months real,
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
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    if mode == "main":
        values = input_field.split(",")
        values[4] = round(float(values[4]), 2)
        c.execute(
            "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ?",
            (values[3], values[5]),
        )
        exists = c.fetchone()
        if exists == None:
            raise Exception("Person_bank-currency pair does not exist!")
        if values[5] > 0:
            c.execute(
                "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ? AND sum > ?",
                (values[3], values[5], values[4]),
            )
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

        records = {keys[i]: values[i] for i in range(len(keys))}

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
        )
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

        records = {tr_keys[i]: values[i] for i in range(len(tr_keys))}

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
        )
        exists = c.fetchone()
        if exists == None:
            raise Exception(
                "Person_bank-currency pair does not exist or insufficient funds!"
            )
        c.execute(
            "SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ?",
            (values[4], values[6]),
        )
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

        records = {advtr_keys[i]: values[i] for i in range(len(advtr_keys))}

        c.execute(
            "INSERT INTO advtransfer VALUES (:id, :date, :person_bank_from, :sum_from, :currency_from, :person_bank_to, :sum_to, :currency_to, :comment)",
            records,
        )

    elif mode == "deposit":
        values = input_field.split(",")
        values[3] = round(float(values[3]), 2)
        if values[5] == " ":
            values[5] = 0
        else:
            values[5] = float(values[5])
        values[7] = float(values[7])
        if values[8] == " ":
            values[8] = 0
        else:
            values[8] = float(values[8])

        if values[5] == 0 or values[6] == " ":
            values.insert(9, 0)
        else:
            percent = values[7] / 100
            expSum = values[3] + (values[3] * (percent / 12) * values[5])
            values.insert(10, round(expSum, 2))

        records = {dp_keys[i]: values[i] for i in range(len(dp_keys))}

        c.execute(
            "INSERT INTO deposit VALUES (:date_in, :name, :owner, :sum, :currency, :months, :date_out, :percent, :currency_rate, :expect, :comment)",
            records,
        )

    conn.commit()
    conn.close()

    Re_calculate()


def Read(x):
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
    elif x == "alldep":
        c.execute("SELECT * FROM deposit ORDER BY date_out DESC")
        return c.fetchall()
    elif x == "allcurr":
        c.execute("SELECT currency, SUM(sum) FROM PB_account GROUP BY currency")
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

    # elif (x == 'catincrep'):
    #     categories_df = pd.read_csv(SPVcatIncPath, header=None)
    #     categories_list = categories_df[0].tolist()

    #     query = 'SELECT category, currency, sum FROM main WHERE category IN ({}) ORDER BY category DESC'.format(','.join('?' for _ in categories_list))
    #     c.execute(query, categories_list)
    #     return c.fetchall()
    # elif (x == 'catexprep'):
    #     categories_df = pd.read_csv(SPVcatExpPath, header=None)
    #     categories_list = categories_df[0].tolist()

    #     query = 'SELECT category, currency, sum FROM main WHERE category IN ({}) ORDER BY category DESC'.format(','.join('?' for _ in categories_list))
    #     c.execute(query, categories_list)
    #     return c.fetchall()

    elif x == "extype":
        c.execute("SELECT DISTINCT type FROM Marker_type")
        return c.fetchall()
    elif x == "exowner":
        c.execute("SELECT DISTINCT owner FROM Marker_owner")
        return c.fetchall()

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

    conn.commit()
    conn.close()


def ReadAdv(type, month):
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

    if type == "catincrep":
        categories_df = pd.read_csv(SPVcatIncPath, header=None)
        categories_list = categories_df[0].tolist()

        query = 'SELECT category, currency, sum FROM main category IN ({}) WHERE strftime("%m", date) = ? ORDER BY category DESC'.format(
            ",".join("?" for _ in categories_list)
        )
        c.execute(query, month, categories_list)
        return c.fetchall()

    if type == "catexprep":
        categories_df = pd.read_csv(SPVcatExpPath, header=None)
        categories_list = categories_df[0].tolist()

        query = 'SELECT category, currency, sum FROM main category IN ({}) WHERE strftime("%m", date) = ? ORDER BY category DESC'.format(
            ",".join("?" for _ in categories_list)
        )
        c.execute(query, month, categories_list)
        return c.fetchall()

    conn.commit()
    conn.close()


def MarkerRead(markers, mode):
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
        values = markers.split(',')
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

    # Check for any person_bank and currency pairs that are missing in the main and transfer tables
    # c.execute('SELECT person_bank, currency FROM PB_account')
    # existing_pairs = c.fetchall()
    # for person_bank, currency in existing_pairs:
    #     c.execute('''
    #         SELECT SUM(sum)
    #         FROM (
    #             SELECT sum FROM main WHERE person_bank = ? AND currency = ?
    #             UNION ALL
    #             SELECT sum FROM Init_PB WHERE person_bank = ? AND currency = ?
    #             UNION ALL
    #             SELECT -sum FROM transfer WHERE person_bank_from = ? AND currency = ?
    #             UNION ALL
    #             SELECT sum FROM transfer WHERE person_bank_to = ? AND currency = ?
    #         )
    #     ''', (person_bank, currency, person_bank, currency, person_bank, currency, person_bank, currency))
    #     total_sum = c.fetchone()[0]
    #     if total_sum is None:
    #         c.execute('UPDATE PB_account SET sum = 0 WHERE person_bank = ? AND currency = ?', (person_bank, currency))

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


def SPVconf(x):
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
    print("Input new values in format: str1,str2,...\n")
    new_SPV = input()
    new_SPV = new_SPV.split(",")

    print(" A - Append\n R - Replace\n")
    choice = input()
    if choice == "A" or choice == "a":
        new_SPV = "," + new_SPV
        with open(path, mode="a", newline="") as file:
            csvWriter = csv.writer(file)
            for i in new_SPV:
                csvWriter.writerow([i])
        print("Success!\n\n")

    elif choice == "R" or choice == "r":
        with open(path, mode="w", newline="") as file:
            csvWriter = csv.writer(file)
            for i in new_SPV:
                csvWriter.writerow([i])
        print("Success!\n\n")

    else:
        print("Unknown command!\n\n")


def InitPB():
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    print("Input new person_bank record in format: person_bank,sum,currency\n")
    new_pb = input()
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
            "SELECT 1 FROM Marker_owner WHERE person_bank = ? AND owner = ?",
            (marker[0], marker[1]),
        )
        exists = c.fetchone()
        if exists != None:
            print("Marker already exists!\n\n")
            return
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
            print("Marker already exists!\n\n")
            return
        else:
            c.execute(
                "INSERT INTO Marker_owner (person_bank, owner) VALUES (?, ?)",
                (marker[0], marker[1]),
            )
            print("Success!\n\n")

    conn.commit()
    conn.close()


def DelPB():
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    print("Delete person_bank record in format: person_bank,currency\n")
    new_pb = input()
    new_pb = new_pb.split(",")

    try:
        c.execute(
            "DELETE FROM PB_account WHERE person_bank = ? AND currency = ?", (new_pb)
        )
    except:
        print("Failure!\n\n")
    print("Success!\n\n")

    conn.commit()
    conn.close()

    Re_calculate()
