import os.path
import sqlite3
from db_scripts.consts import *


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
    if not os.path.exists(dbPath):
        return 1

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in c.fetchall()]
        missing_tables = []
        for table in expected_tables.keys():
            if table not in existing_tables:
                missing_tables.append(table)
        if missing_tables:
            print(f"Missing tables: {missing_tables}")
            return 2

        if CheckDBLegacy() == -1:
            return -1
        if CheckDBStructure() == -3:
            return 3
        return 0


def CheckDBStructure():
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()
        # Verify table structures
        for table, expected_columns in expected_tables.items():
            c.execute(f"PRAGMA table_info({table})")
            actual_columns = [row[1] for row in c.fetchall()]
            # Check if all expected columns exist
            for column in expected_columns:
                if column not in actual_columns:
                    print(f"Table {table} missing column: {column}")
                    return 3


def CheckDBLegacy():
    global isLegacyCurrencyRates
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()
        for table, old_columns in old_tables.items():
            c.execute(f"PRAGMA table_info({table})")
            actual_columns = [row[1] for row in c.fetchall()]

            # Check if all old columns exist in the actual table
            if set(old_columns).issubset(set(actual_columns)):
                print(f"Legacy table {table} found! Switching to legacy mode")
                isLegacyCurrencyRates = True
                return -1
        return 0
