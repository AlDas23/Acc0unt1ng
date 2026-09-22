import os.path
import shutil
import sqlite3
import db_scripts.consts as consts
from helpers.configScripts import AddToBackupYears


def NewDBase():
    # Create or replace DB file using template
    directory = os.path.dirname(consts.dbPath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(consts.dbPath):
        os.remove(consts.dbPath)

    with sqlite3.connect(consts.dbPath) as conn:
        c = conn.cursor()

        c.execute("""CREATE TABLE main (
                    id integer PRIMARY KEY,
                    date text,
                    category text,
                    sub_category text,
                    person_bank text,
                    sum real,
                    currency text,
                    comment text
                )""")
        c.execute("""CREATE TABLE exc_rate (
                    id integer PRIMARY KEY,
                    date text,
                    currency_M text,
                    currency_S text,
                    rate real
                )""")
        c.execute("""CREATE TABLE deposit (
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
                )""")
        c.execute("""CREATE TABLE transfer (
                    id integer,
                    date text,
                    person_bank_from text,
                    person_bank_to text,
                    sum real,
                    currency text,
                    comment text
                )""")
        c.execute("""CREATE TABLE advtransfer (
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
                )""")
        c.execute("""CREATE TABLE Init_PB (
                    person_bank text,
                    sum real,
                    currency text
                )""")
        c.execute("""CREATE TABLE Marker_owner (
                    bank_rec text,
                    owner text
                )""")
        c.execute("""CREATE TABLE Marker_type (
                    bank_rec text,
                    type text
                )""")
        c.execute("""CREATE TABLE Planning (
                    id integer PRIMARY KEY,
                    date text,
                    comment text,
                    person_bank text,
                    sum real,
                    currency text      
                )""")
        # Invest tables
        c.execute("""CREATE TABLE investTransaction (
                    id integer PRIMARY KEY,
                    date text,
                    PB text,
                    amount real,
                    currency text,
                    investPB text,
                    investAmount real,
                    stock text, 
                    fee real
                )""")
        c.execute("""CREATE TABLE investPB (
                    name text,
                    stock text
                )""")
        c.execute("""CREATE TABLE investStockPrice (
                    id integer PRIMARY KEY,
                    date text,
                    stock text,
                    price real,
                    currency text
                )""")

        conn.commit()


def CheckDB():
    if not os.path.exists(consts.dbPath):
        return 1

    with sqlite3.connect(consts.dbPath) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in c.fetchall()]
        missing_tables = []
        for table in consts.expected_tables.keys():
            if table not in existing_tables:
                missing_tables.append(table)
        if missing_tables:
            if "planning" in missing_tables:
                UpdateDB("planning")
                missing_tables.remove("planning")
            print(f"Missing tables: {missing_tables}")
            return 2

        if CheckDBLegacy() == -1:
            return -1
        if CheckDBStructure() == 3:
            return 3
        return 0


def CheckDBStructure():
    with sqlite3.connect(consts.dbPath) as conn:
        c = conn.cursor()
        # Verify table structures
        for table, expected_columns in consts.expected_tables.items():
            c.execute(f"PRAGMA table_info({table})")
            actual_columns = [row[1] for row in c.fetchall()]
            # Check if all expected columns exist
            for column in expected_columns:
                if column not in actual_columns:
                    print(f"Table {table} missing column: {column}")
                    return 3


def CheckDBLegacy():
    with sqlite3.connect(consts.dbPath) as conn:
        c = conn.cursor()

        legacy_tables_found = []

        for table, old_columns in consts.old_tables.items():
            c.execute(f"PRAGMA table_info({table})")
            actual_columns = [row[1] for row in c.fetchall()]

            # Check if all old columns exist in the actual table
            if set(old_columns) == set(actual_columns):
                print(f"Legacy table {table} found!")
                legacy_tables_found.append(table)

        if "investStockPrice" in legacy_tables_found:
            UpdateDB("investStockPrice")
            return 0

        if legacy_tables_found:
            return -1
        return 0


def UpdateDB(mode):
    if consts.mainCurrency == None:
        raise Exception("Main currency not set! Can't update DB")

    if mode == "planning":
        with sqlite3.connect(consts.dbPath) as conn:
            c = conn.cursor()

            # Add new Planning table
            c.execute("""CREATE TABLE Planning (
                        id integer PRIMARY KEY,
                        date text,
                        comment text,
                        person_bank text,
                        sum real,
                        currency text      
                    )""")
            conn.commit()
            print("Created new Planning table")
            return 0

    elif mode == "investStockPrice":
        with sqlite3.connect(consts.dbPath) as conn:
            c = conn.cursor()

            # Drop old investStockPrice table
            c.execute("DROP TABLE IF EXISTS investStockPrice")
            conn.commit()
            print("Removed old investStockPrice table")

            # Add new investStockPrice table
            c.execute("""CREATE TABLE investStockPrice (
                        id integer PRIMARY KEY,
                        date text,
                        stock text,
                        price real,
                        currency text
                    )""")
            conn.commit()
            print("Created new investStockPrice table")
            return 0


def BackupDB():
    directory = os.path.dirname(consts.dbArchivePath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    shutil.copy2(consts.dbPath, consts.dbArchivePath)
    print("Database backup created")

    os.rename(
        os.path.join(consts.dbArchivePath, "Main.db"),
        os.path.join(consts.dbArchivePath, f"Main_{consts.currentYear - 1}.db"),
    )
    print(f"Database backup renamed to Main_{consts.currentYear - 1}.db")


def UpdateDBYear():
    if consts.mainCurrency == None:
        raise Exception("Main currency not set! Can't update DB")

    BackupDB()

    with sqlite3.connect(consts.dbPath) as conn:
        c = conn.cursor()

        # Colloct new initial balances
        c.execute("SELECT DISTINCT person_bank FROM Init_PB")
        person_banks = c.fetchall()
        person_banks = [pb[0] for pb in person_banks]
        seq = ",".join(["?"] * len(person_banks))
        previousYear = consts.currentYear - 1
        previousYearStr = str(previousYear)
        c.execute(
            f"""
                SELECT person_bank, ROUND(SUM(sum), 2) AS sum, currency
                FROM (
                    -- Main accounts and transfers
                    SELECT person_bank, currency, sum FROM main WHERE strftime('%Y', date) = ?
                    UNION ALL
                    SELECT person_bank, currency, sum FROM Init_PB
                    UNION ALL
                    SELECT person_bank_from AS person_bank, currency, -sum FROM transfer WHERE strftime('%Y', date) = ?
                    UNION ALL
                    SELECT person_bank_from AS person_bank, currency_from AS currency, -sum_from AS sum FROM advtransfer WHERE strftime('%Y', date) = ?
                    UNION ALL
                    SELECT person_bank_to AS person_bank, currency_to AS currency, sum_to AS sum FROM advtransfer WHERE strftime('%Y', date) = ?
                    UNION ALL
                    SELECT person_bank_to AS person_bank, currency, sum FROM transfer WHERE strftime('%Y', date) = ?
                    
                    -- PBD logic is ignored since new balance should be full, only later deposits are deducted
                )
                WHERE person_bank IN ({seq})
                GROUP BY person_bank, currency
                """,
            (
                previousYearStr,
                previousYearStr,
                previousYearStr,
                previousYearStr,
                previousYearStr,
                *person_banks,
            ),
        )
        newInitPBData = c.fetchall()

        # Clear old Init_PB table
        c.execute("DELETE FROM Init_PB")

        # Insert new initial balances
        c.executemany(
            "INSERT INTO Init_PB (person_bank, sum, currency) VALUES (?, ?, ?)",
            newInitPBData,
        )

        conn.commit()
    print("Updated initial balances for the new year")
    AddToBackupYears(previousYear)
    print("Updated config backup years")
