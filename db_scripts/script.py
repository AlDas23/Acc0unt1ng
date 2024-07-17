import os.path
import sqlite3
from db_scripts.consts import *


def NewDBase():
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    
    c.execute("""CREATE TABLE main (
                id integer,
                date text,
                sum real,
                category text,
                sub_category text,
                comment text,
                person_bank text,
                currency text
            )""")
    conn.commit()
    conn.close()

def Add(input_field):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    
    c.execute("SELECT MAX(id) FROM main")
    max_id = c.fetchone()
    max_id = max_id[0]
    if (max_id == None):
        values = input_field.split(",")
        values.insert(0, 1)
    else:
        values = input_field.split(",")
        values.insert(0, max_id[id] + 1) # Change so that inserted number is +1 from biggest existing id in DB
    
    values[2] = float(values[2])
    records = {keys[i]: values[i] for i in range(len (keys))}
    
    c.execute("INSERT INTO main VALUES (:id, :date, :sum, :category, :sub_category, :comment, :person_bank, :currency)",
              records)
    
    conn.commit()
    conn.close()

def Read():
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    
    c.execute("SELECT * FROM main")
    print(c.fetchall())
    
    conn.commit()
    conn.close()

def Del(del_id):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    
    
    conn.commit()
    conn.close()