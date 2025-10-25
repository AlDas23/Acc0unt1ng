import os.path
import sqlite3
import db_scripts.consts as consts


def NewDBase():
    # Create or replace DB file using template
    directory = os.path.dirname(consts.dbPath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(consts.dbPath):
        os.remove(consts.dbPath)

    with sqlite3.connect(consts.dbPath) as conn:
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
                    id integer PRIMARY KEY,
                    date text,
                    currency_M text,
                    currency_S text,
                    rate real
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
        for table, old_columns in consts.old_tables.items():
            c.execute(f"PRAGMA table_info({table})")
            actual_columns = [row[1] for row in c.fetchall()]

            # Check if all old columns exist in the actual table
            if set(old_columns).issubset(set(actual_columns)):
                print(f"Legacy table {table} found! Switching to legacy mode")
                consts.isLegacyCurrencyRates = True
                return -1
        return 0


def UpdateDB():
    if consts.mainCurrency == None:
        raise Exception("Main currency not set! Can't update DB")

    if consts.isLegacyCurrencyRates == False:
        raise Exception("DB is already up to date! Can't update DB")
    else:
        print("Initiate DB update...\n")
        with sqlite3.connect(consts.dbPath) as conn:
            c = conn.cursor()

            # Collect all data from old exc_rate table
            c.execute("SELECT * FROM exc_rate")
            old_rates = c.fetchall()
            print("Saved old exhange rates")

            # Drop old exc_rate table
            c.execute("DROP TABLE IF EXISTS exc_rate")
            conn.commit()
            print("Removed old table")

            # Create new exc_rate table
            c.execute(
                """CREATE TABLE exc_rate (
                        id integer PRIMARY KEY,
                        date text,
                        currency_M text,
                        currency_S text,
                        rate real
                    )"""
            )
            conn.commit()
            print("Created new table")

            # Migrate old data to new exc_rate table
            new_rates = []
            for rate in old_rates:
                date, currency_S, curr_rate = rate
                if currency_S == consts.mainCurrency:
                    continue  # Skip rates that are already in main currency
                new_rates.append((date, consts.mainCurrency, currency_S, curr_rate))

            c.executemany(
                "INSERT INTO exc_rate (id, date, currency_M, currency_S, rate) VALUES (NULL, ?, ?, ?, ?)",
                new_rates,
            )
            conn.commit()
            print("Migrated old data to new table")

            # Read new exc_rate table
            c.execute("SELECT * FROM exc_rate")
            all_rates = c.fetchall()
            print(f"Total {len(all_rates)} exchange rates in new table")
            print("DB update completed successfully")
            consts.isLegacyCurrencyRates = False

            return 0
