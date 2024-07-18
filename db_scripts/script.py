import os.path
import sqlite3
from db_scripts.consts import *


def NewDBase():
    if os.path.exists(dbPath):
        os.remove(dbPath)
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    
    c.execute("""CREATE TABLE main (
                id integer,
                date text,
                category text,
                sub_category text,
                person_bank text,
                comment text,
                sum real,
                currency text
            )""")
    c.execute("""CREATE TABLE transfer (
                id integer,
                date text,
                person_bank_from text,
                person_bank_to text,
                comment text,
                sum real,
                currency text
            )""")
    c.execute("""CREATE TABLE PB_account (
                person_bank text,
                sum real,
                currency text
            )""")
    conn.commit()
    conn.close()

def Add(input_field, mode):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    if (mode == 'main'):
        c.execute("SELECT MAX(id) FROM main")
        max_id = c.fetchone()
        max_id = max_id[0]
        if (max_id == None): # Check if it is exist and change to 0 if not
            max_id = 0
        max_id = max_id + 1 # Change so that inserted number is +1 from biggest existing id in DB
        values = input_field.split(",")
        values.insert(0, max_id)
        
        values[6] = float(values[6])
        records = {keys[i]: values[i] for i in range(len (keys))}
        
        c.execute("INSERT INTO main VALUES (:id, :date, :category, :sub_category, :person_bank, :comment, :sum, :currency)",
                records)
        
        conn.commit()
        conn.close()
        
        Re_calculate(max_id, 'M') 
        
    elif (mode == 'transfer'):
        c.execute("SELECT MAX(id) FROM transfer")
        max_id = c.fetchone()
        max_id = max_id[0]
        if (max_id == None): # Check if it is exist and change to 0 if not
            max_id = 0
        max_id = max_id + 1 # Change so that inserted number is +1 from biggest existing id in DB
        values = input_field.split(",")
        values.insert(0, max_id)
        
        values[5] = float(values[5]) 
        if (values[5] < 0): # Make sum positive if not
            values[5] = values[5] * -1
        records = {tr_keys[i]: values[i] for i in range(len (tr_keys))}
        
        c.execute("INSERT INTO transfer VALUES (:id, :date, :person_bank_from, :person_bank_to, :comment, :sum, :currency)",
                records)
        
        conn.commit()
        conn.close()
        
        Re_calculate(max_id, 'T')

def Read(x):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    
    if (x == 'allm'):
        c.execute("SELECT * FROM main")
        print(c.fetchall())
    elif (x == 'allacc'):
        c.execute("SELECT * FROM PB_account")
        print(c.fetchall())
    elif (x == 'alltran'):
        c.execute("SELECT * FROM transfer")
        print(c.fetchall())
        
    conn.commit()
    conn.close()

def Del(del_id):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    
    c.execute("DELETE FROM main WHERE id = ?", (del_id,))
    
    conn.commit()
    conn.close()
    
def Re_calculate(id, mode):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    if (mode == 'M'): # Re-caculate called from Add-main
        c.execute("SELECT person_bank, sum, currency FROM main WHERE id = ?", (id,))
        x = c.fetchone()
        pb = x[0]
        sum = x[1]
        curr = x[2]
        
        c.execute("SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ?", (pb, curr))
        exists = c.fetchone()
        if (exists != None):
            c.execute("SELECT sum FROM PB_account WHERE person_bank = ?", (pb,))
            temp = c.fetchone()
            sum += temp[0]
            c.execute("UPDATE PB_account SET sum = ? WHERE person_bank = ?", (sum, pb))
        else:
            c.execute("INSERT INTO PB_account (person_bank, sum, currency) VALUES (?, ?, ?)", (pb, sum, curr))
        
    elif (mode == 'T'): # Re-caculate called from Add-transfer
        c.execute("SELECT person_bank_from, person_bank_to, sum, currency FROM transfer WHERE id = ?", (id,))
        x = c.fetchone()
        pb_out = x[0]
        pb_in = x[1]
        sum = x[2]
        curr = x[3]
        
        c.execute("SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ?", (pb_out, curr))
        exists = c.fetchone()
        if (exists == None):
            c.execute("DELETE FROM transfer WHERE id = ?", (id,))
            print("Impossible to send tranfer from non-existent account!\n")
        else:
            c.execute("SELECT sum FROM PB_account WHERE person_bank = ?", (pb_out,))
            temp = c.fetchone()
            sum1 = temp[0] - sum
            c.execute("UPDATE PB_account SET sum = ? WHERE person_bank = ?", (sum1, pb_out))
                
            c.execute("SELECT 1 FROM PB_account WHERE person_bank = ? AND currency = ?", (pb_in, curr))
            exists = c.fetchone()
            if (exists != None):
                c.execute("SELECT sum FROM PB_account WHERE person_bank = ?", (pb_in,))
                temp = c.fetchone()
                sum2 = sum + temp[0]
                c.execute("UPDATE PB_account SET sum = ? WHERE person_bank = ?", (sum2, pb_in))
            else:
                c.execute("INSERT INTO PB_account (person_bank, sum, currency) VALUES (?, ?, ?)", (pb_in, sum, curr))
                
    conn.commit()
    conn.close()