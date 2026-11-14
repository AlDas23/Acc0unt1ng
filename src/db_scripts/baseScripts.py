from datetime import datetime, timedelta
import sqlite3
from db_scripts.consts import *
import db_scripts.consts as consts
from db_scripts.enums import ReadType, TransactionType


def NewAdd(recordDict, type):
    """Upgraded version of Add(input_field, mode).

    Args:
        recordDict (dict): Dictionary with all values to add
        type (TransactionType): Enum parameter for selecting into which table to add the record.
    """
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        if type == TransactionType.MAIN:
            if recordDict["personBank"] != "":
                c.execute(
                    "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
                    (recordDict["personBank"], recordDict["currency"]),
                )
                exists = c.fetchone()
                if exists is None:
                    raise Exception("Person_bank-currency pair does not exist!")

            recordDict["sum"] = round(float(recordDict["sum"]), 2)

            c.execute(
                "INSERT INTO main VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                (
                    recordDict["date"],
                    recordDict["category"],
                    recordDict.get("subCategory", ""),
                    recordDict["personBank"],
                    recordDict["sum"],
                    recordDict["currency"],
                    recordDict.get("comment", ""),
                ),
            )
            
        elif type == TransactionType.TRANSFER:
            if recordDict["Sender"] != "":
                c.execute(
                    "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
                    (recordDict["Sender"], recordDict["Currency"]),
                )
                exists = c.fetchone()
                if exists is None:
                    raise Exception("Person_bank-currency pair does not exist!")

            if recordDict["Receiver"] != "":
                c.execute(
                    "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
                    (recordDict["Receiver"], recordDict["Currency"]),
                )
                exists = c.fetchone()
                if exists is None:
                    raise Exception("Person_bank-currency pair does not exist!")

            recordDict["Sum"] = round(float(recordDict["Sum"]), 2)

            c.execute(
                "INSERT INTO transfer VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                (
                    recordDict["Date"],
                    recordDict["Sender"],
                    recordDict["Receiver"],
                    recordDict["Sum"],
                    recordDict["Currency"],
                    recordDict.get("Comment", ""),
                ),
            )
            
        elif type == TransactionType.ADVTRANSFER:
            if recordDict["ADVSender"] != "":
                c.execute(
                    "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
                    (recordDict["ADVSender"], recordDict["SCurrency"]),
                )
                exists = c.fetchone()
                if exists is None:
                    raise Exception("Person_bank-currency pair does not exist!")

            if recordDict["ADVReceiver"] != "":
                c.execute(
                    "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
                    (recordDict["ADVReceiver"], recordDict["RCurrency"]),
                )
                exists = c.fetchone()
                if exists is None:
                    raise Exception("Person_bank-currency pair does not exist!")

            recordDict["SSum"] = round(float(recordDict["SSum"]), 2)
            recordDict["RSum"] = round(float(recordDict["RSum"]), 2)
            if recordDict["CurrencyRate"] != '':
                recordDict["CurrencyRate"] = round(float(recordDict["CurrencyRate"]), 4)

            c.execute(
                "INSERT INTO advtransfer VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    recordDict["ADVDate"],
                    recordDict["ADVSender"],
                    recordDict["SSum"],
                    recordDict["SCurrency"],
                    recordDict["ADVReceiver"],
                    recordDict["RSum"],
                    recordDict["RCurrency"],
                    recordDict["CurrencyRate"],
                    recordDict.get("ADVComment", ""),
                ),
            )
            
        elif type == TransactionType.DEPOSIT:
            if recordDict["Owner"] != "":
                c.execute(
                    "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
                    (recordDict["Owner"], recordDict["Currency"]),
                )
                exists = c.fetchone()
                if exists is None:
                    raise Exception("Person_bank-currency pair does not exist!")

            recordDict["Sum"] = round(float(recordDict["Sum"]), 2)
            if recordDict["Months"] == "":
                recordDict["Months"] = 0
            else:
                recordDict["Months"] = int(recordDict["Months"])
            recordDict["Percent"] = float(recordDict["Percent"])
            if recordDict["CurrencyRate"] == "":
                recordDict["CurrencyRate"] = 0
            else:
                recordDict["CurrencyRate"] = float(recordDict["CurrencyRate"])

            if recordDict["Months"] == 0 or recordDict["DateOut"] == "":
                recordDict["Expect"] = 0
                recordDict["IsOpen"] = 0
            else:
                # Provided formula to calculate deposit return
                percent = recordDict["Percent"] / 100
                expSum = recordDict["Sum"] + (
                    recordDict["Sum"] * (percent / 12) * recordDict["Months"]
                )
                recordDict["Expect"] = round(expSum, 2)
                recordDict["IsOpen"] = 1

            c.execute(
                "INSERT INTO deposit VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    recordDict["DateIn"],
                    recordDict["Name"],
                    recordDict["Owner"],
                    recordDict["Sum"],
                    recordDict["Currency"],
                    recordDict["Months"],
                    recordDict["DateOut"],
                    recordDict["Percent"],
                    recordDict["CurrencyRate"],
                    recordDict["Expect"],
                    recordDict.get("Comment", ""),
                    recordDict["IsOpen"],
                ),)
            
            c.execute("INSERT INTO Marker_type VALUES(?, ?)", (recordDict["Name"], "deposit"))
            
        elif type == TransactionType.CURRRATE:
            recordDict["rate"] = round(float(recordDict["rate"]), 4)
            
            if recordDict["isReverse"] == True:
                reverseRate = round(1 / float(recordDict["rate"]), 4)

                reverseValues = {
                    "date": recordDict["date"],
                    "currency_M": recordDict["currency_S"],
                    "currency_S": recordDict["currency_M"],
                    "rate": reverseRate
                }
                
            c.execute(
                "INSERT INTO exc_rate VALUES (NULL, ?, ?, ?, ?)",
                (
                    recordDict["date"],
                    recordDict["currency_M"],
                    recordDict["currency_S"],
                    recordDict["rate"],
                ),
            )
            
            if recordDict["isReverse"] == True:
                            c.execute(
                                "INSERT INTO exc_rate VALUES (NULL, ?, ?, ?, ?)",
                                (reverseValues["date"], reverseValues["currency_M"], reverseValues["currency_S"], reverseValues["rate"]),
                            )
        
        elif type == TransactionType.PLANNING:
            if recordDict["personBank"] != "":
                c.execute(
                    "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
                    (recordDict["personBank"], recordDict["currency"]),
                )
                exists = c.fetchone()
                if exists is None:
                    raise Exception("Person_bank-currency pair does not exist!")

            recordDict["sum"] = round(float(recordDict["sum"]), 2)

            c.execute(
                "INSERT INTO planning VALUES (NULL, ?, ?, ?, ?, ?)",
                (
                    recordDict["date"],
                    recordDict["comment"],
                    recordDict["personBank"],
                    recordDict["sum"],
                    recordDict["currency"],
                ),
            )

        conn.commit()
        
        Re_Calculate_deposit()
        
def ReadNew(x, year=None, skipArchivedPBs=True):
    """Upgraded version of Read(x, year=None).
    
        Args:
            x ReadType (enum): Type of data to read
            year (int, optional): Year to filter by
            skipArchivedPBs (bool): Whether to skip archived person banks
        """
    data = []
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        if x == ReadType.INITPB:
            c.execute("SELECT * FROM Init_PB ORDER BY person_bank DESC")
            data = c.fetchall()
        elif x == ReadType.DINITPB:
            c.execute("SELECT DISTINCT person_bank FROM Init_PB ORDER BY person_bank DESC")
            if skipArchivedPBs:
                for row in c.fetchall():
                    if row[0] not in consts.archivedPBs:
                        data.append(row[0])
            else:
                data = [row[0] for row in c.fetchall()]
        elif x == ReadType.CAT:
            c.execute("SELECT DISTINCT category FROM main ORDER BY category DESC")
            data = [row[0] for row in c.fetchall()]
        elif x == ReadType.CATINC:
            c.execute("SELECT DISTINCT category FROM main WHERE sum > 0 ORDER BY category DESC")
            data = [row[0] for row in c.fetchall()]
        elif x == ReadType.CATEXP:
            c.execute("SELECT DISTINCT category FROM main WHERE sum < 0 ORDER BY category DESC")
            data = [row[0] for row in c.fetchall()]
        
            
    return data


def Read(x, year=None):
    # Big collection of queries for returning different data from DB
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        if x == "allm":
            c.execute("SELECT * FROM main")
            return c.fetchall()
        elif x == "m+":
            c.execute(
                "SELECT id, date, category, person_bank, sum, currency, comment FROM main WHERE sum > 0 AND strftime('%Y', date) = ? ORDER BY date DESC, id DESC",
                (year,),
            )
            return c.fetchall()
        elif x == "m-":
            c.execute(
                "SELECT * FROM main WHERE sum < 0 AND strftime('%Y', date) = ? ORDER BY date DESC, id DESC",
                (year,),
            )
            return c.fetchall()
        elif x == "initpb":
            raise Exception("Obsolete query. Use ReadNew().")
        elif x == "initpbnames":
            raise Exception("Obsolete query. Use ReadNew().")
        elif x == "allacc":
            c.execute("""
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
                """)
            return c.fetchall()
        elif x == "alldep":
            c.execute("SELECT * FROM deposit ORDER BY date_out DESC")
            return c.fetchall()
        elif x == "opendep":
            c.execute(
                "SELECT date_in, name, owner, sum, currency, months, date_out, percent, currency_rate, expect, comment FROM deposit WHERE isOpen = 1 ORDER BY date_out ASC"
            )
            return c.fetchall()
        elif x == "closeddep":
            c.execute(
                "SELECT date_in, name, owner, sum, currency, months, date_out, percent, currency_rate, expect, comment FROM deposit WHERE isOpen = 0 ORDER BY date_out DESC",
            )
            return c.fetchall()
        elif x == "alltran":
            c.execute(
                "SELECT * FROM transfer WHERE strftime('%Y', date) = ? ORDER BY date DESC",
                (year,),
            )
            return c.fetchall()
        elif x == "alladvtran":
            c.execute(
                "SELECT * FROM advtransfer WHERE strftime('%Y', date) = ? ORDER BY date DESC",
                (year,),
            )
            return c.fetchall()
        elif x == "planning":
            c.execute("SELECT * FROM planning ORDER BY date, id DESC")
            return c.fetchall()
        elif x == "allcurr":
            c.execute(
                """
                    SELECT currency, ROUND(SUM(total_sum), 2) AS total_amount
                    FROM (
                        SELECT currency, sum AS total_sum FROM Init_PB
                        
                        UNION ALL
                        
                        SELECT currency, sum AS total_sum FROM main WHERE strftime('%Y', date) = ?
        
                        UNION ALL
        
                        SELECT currency_from AS currency, -sum_from AS total_sum FROM advtransfer WHERE strftime('%Y', date) = ?
        
                        UNION ALL
        
                        SELECT currency_to AS currency, sum_to AS total_sum FROM advtransfer WHERE strftime('%Y', date) = ?
                    ) AS combined
                    GROUP BY currency    
                """,
                (year, year, year),
            )
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
                        WHERE
                                strftime('%Y', date) = ?
                        GROUP BY
                            mt.person_bank, currency

                        UNION ALL

                        SELECT
                            tr.person_bank_from AS person_bank,
                            currency,
                            -SUM(tr.sum) AS normal_balance
                        FROM
                            transfer AS tr
                        WHERE
                            strftime('%Y', date) = ?
                        GROUP BY
                            tr.person_bank_from, currency

                        UNION ALL

                        SELECT
                            tr.person_bank_to AS person_bank,
                            currency,
                            SUM(tr.sum) AS normal_balance
                        FROM
                            transfer AS tr
                        WHERE
                            strftime('%Y', date) = ?
                        GROUP BY
                            tr.person_bank_to, currency

                        UNION ALL

                        SELECT
                            at.person_bank_from AS person_bank,
                            currency_from AS currency,
                            -SUM(at.sum_from) AS normal_balance
                        FROM
                            advtransfer AS at
                        WHERE
                            strftime('%Y', date) = ?    
                        GROUP BY
                            at.person_bank_from, currency_from

                        UNION ALL

                        SELECT
                            at.person_bank_to AS person_bank,
                            currency_to AS currency,
                            SUM(at.sum_to) AS normal_balance
                        FROM
                            advtransfer AS at
                        WHERE
                            strftime('%Y', date) = ?
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
                    """,
                (year, year, year, year, year),
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
                            WHERE
                                strftime('%Y', date) = ?
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
                            WHERE
                                strftime('%Y', date) = ?
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
                            WHERE
                                strftime('%Y', date) = ?
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
                            WHERE
                                strftime('%Y', date) = ?
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
                            WHERE
                                strftime('%Y', date) = ?
                            GROUP BY
                                at.person_bank_to, currency_to
                        ) AS all_normal_balances
                        GROUP BY person_bank, currency
                    ) AS all_normal_balances ON m.bank_rec = all_normal_balances.person_bank
                    GROUP BY 
                        m.owner, 
                        all_normal_balances.currency
                """,
                (year, year, year, year, year),
            )
            return c.fetchall()

        elif x == "extype":
            c.execute("SELECT DISTINCT type FROM Marker_type WHERE type != 'deposit'")
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
                    substr(strftime('%Y-%m', date), 3, 5) AS month, 
                    date, 
                    sum,
                    currency
                FROM main
                WHERE strftime('%Y', date) = ?
                ORDER BY month
                """,
                (year,),
            )
            return c.fetchall()

        elif x == "yearexp":
            c.execute(
                """
                SELECT 
                    substr(strftime('%Y-%m', date), 3, 5) AS month,
                    currency,
                    ABS(sum) AS expense,
                    "date"
                FROM main
                WHERE sum < 0 AND strftime('%Y', date) = ?
                ORDER BY month
                """,
                (year,),
            )
            return c.fetchall()

        elif x == "yearinc":
            c.execute(
                """
                    SELECT 
                    substr(strftime('%Y-%m', date), 3, 5) AS month,
                    currency,
                    ABS(sum) AS expense,
                    "date"
                FROM main
                WHERE sum > 0 AND strftime('%Y', date) = ?
                ORDER BY month
                    """,
                (year,),
            )
            return c.fetchall()

        elif x == "retacc":  # Return list of all accounts
            raise Exception("Obsolete query. Use ReadNew().")

        elif x == "retmowner":  # Return list of all owners
            c.execute("SELECT DISTINCT owner FROM Marker_owner")
            result = [row[0] for row in c.fetchall()]
            return result

        elif x == "retmtype":  # Return list of all types
            c.execute("SELECT DISTINCT type FROM Marker_type")
            result = [row[0] for row in c.fetchall()]
            return result

        elif x == "currrate":
            c.execute(
                "SELECT id, substr(strftime('%Y-%m-%d', date), 3, 8), currency_M, currency_S, rate FROM exc_rate WHERE strftime('%Y', date) = ? ORDER BY date DESC",
                (year,),
            )
            return c.fetchall()

        elif x == "currrateplot":
            yearAgo = datetime.today() - timedelta(days=365)

            c.execute(
                "SELECT date, currency_S AS currency, rate FROM exc_rate WHERE currency_M = ? AND date >= ? ORDER BY date DESC",
                (consts.mainCurrency, yearAgo),
            )
            return c.fetchall()

        elif x == "currrateplotinv":
            yearAgo = datetime.today() - timedelta(days=365)

            c.execute(
                "SELECT date, currency_M AS currency, rate FROM exc_rate WHERE currency_S = ? AND date >= ? ORDER BY date DESC",
                (consts.mainCurrency, yearAgo),
            )
            return c.fetchall()

        elif x == "currratenamesinv":
            c.execute(
                "SELECT DISTINCT currency_M AS currency FROM exc_rate WHERE currency_S = ? ORDER BY date DESC",
                (consts.mainCurrency,),
            )
            return [row[0] for row in c.fetchall()]

        elif x == "retcat":
            raise Exception("Obsolete query. Use ReadNew().")

        elif x == "retcat+":
            raise Exception("Obsolete query. Use ReadNew().")

        elif x == "retcat-":
            raise Exception("Obsolete query. Use ReadNew().")


def MarkerRead(mode, markers=None, showArchived=False):
    # Function for returning markers sums for type/owner/both markers
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        person_banks = []
        currentYear = str(consts.currentYear)

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
            person_banks = [row[0] for row in c.fetchall()]

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
            person_banks = [row[0] for row in c.fetchall()]

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
            person_banks = [row[0] for row in c.fetchall()]
            
        elif mode == "none":
            # If no markers are provided, return all person banks
            person_banks = ReadNew(ReadType.DINITPB, skipArchivedPBs=not showArchived)

        if person_banks:
            # Prepare dynamic query to calculate balances using person_banks
            seq = ",".join(["?"] * len(person_banks))

            # This query combines the balances from multiple sources and also integrates PBD logic
            c.execute(
                f"""
        SELECT person_bank, currency, ROUND(SUM(sum), 2) AS sum
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
            
            -- PBD logic
            UNION ALL
            SELECT owner AS person_bank, currency, -sum FROM deposit WHERE isOpen = 1
        )
        WHERE person_bank IN ({seq})
        GROUP BY person_bank, currency
    """,
                (
                    currentYear,
                    currentYear,
                    currentYear,
                    currentYear,
                    currentYear,
                    *person_banks,
                ),
            )

            results = c.fetchall()
            
            if showArchived:
                return results
            else:
                return [row for row in results if row[0] not in consts.archivedPBs]
        else:
            return []


def DelRecord(id, table):
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()
        if table != "deposit":
            c.execute(f"SELECT COUNT(1) FROM {table} WHERE id = ?", (id,))
        else:
            c.execute(f"SELECT COUNT(1) FROM {table} WHERE name = ?", (id,))
        count = c.fetchone()[0]
        if count == 0:
            raise ValueError("Record with the specified ID does not exist.")
        if table != "deposit":
            c.execute(f"DELETE FROM {table} WHERE id = ?", (id,))
        else:
            c.execute(f"DELETE FROM {table} WHERE name = ?", (id,))
            # Cleanup Marker_type
            c.execute(
                f"DELETE FROM Marker_type WHERE bank_rec = ? AND type = ?",
                (id, "deposit"),
            )
        conn.commit()


def Re_Calculate_deposit():
    # Function for calculating if deposit is due or not
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        # Check active deposits and create income/expense if due
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Fetch active deposits from the deposit table where isOpen = 1 and the deposit is not expired
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

            # Mark the deposit as processed
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


def InitPB(name, sum, curr):
    # Person_bank initialization function
    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        c.execute(
            "SELECT 1 FROM Init_PB WHERE person_bank = ? AND currency = ?",
            (name, curr),
        )
        exists = c.fetchone()
        if exists != None:
            raise Exception("PB - Currency combination already exists!")
        else:
            c.execute(
                "INSERT INTO Init_PB (person_bank, sum, currency) VALUES (?, ?, ?)",
                (name, sum, curr),
            )

        conn.commit()

    return


def Mark(pb, owner=None, type=None):
    # Function pushing special record into DB with marker: whose or what type of account is this
    if owner == None and type == None:
        print("At least one marker is required")
        return 1

    with sqlite3.connect(dbPath) as conn:
        c = conn.cursor()

        c.execute(
            "SELECT 1 FROM Init_PB pb WHERE pb.person_bank = ?",
            (pb,),
        )
        exists = c.fetchone()
        if exists is None:
            print("Account record does not exist!\n\n")
            return

        if type != None:
            c.execute("SELECT 1 FROM Marker_type WHERE bank_rec = ?", (pb,))
            exists = c.fetchone()
            if exists != None:
                c.execute(
                    "UPDATE Marker_type SET bank_rec = ?, type = ? WHERE bank_rec = ?",
                    (pb, type, pb),
                )
            else:
                c.execute(
                    "INSERT INTO Marker_type (bank_rec, type) VALUES (?, ?)",
                    (pb, type),
                )
                print("Success!\n\n")

        if owner != None:
            c.execute("SELECT 1 FROM Marker_owner WHERE bank_rec = ?", (pb,))
            exists = c.fetchone()
            if exists != None:
                c.execute(
                    "UPDATE Marker_owner SET bank_rec = ?, owner = ? WHERE bank_rec = ?",
                    (pb, owner, pb),
                )
            else:
                c.execute(
                    "INSERT INTO Marker_owner (bank_rec, owner) VALUES (?, ?)",
                    (pb, owner),
                )

        conn.commit()

        return 0


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
