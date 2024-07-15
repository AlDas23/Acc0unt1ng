import os.path
from io import BytesIO
from fastavro import schemaless_writer, reader
from db_scripts.consts import *


def Add(input_field):
    values = input_field.split(",")
    values.insert(0, 1)
    records = {keys[i]: values[i] for i in range(len (keys))}

    if (os.path.exists(dbPath) == True):
        with open(dbPath, 'a+b') as out:
            schemaless_writer(out, parsed_schema, records)
    else:
        with open(dbPath, 'wb') as out:
            schemaless_writer(out, parsed_schema, records)

def Read():
    with open(dbPath, 'rb') as fo:
        avro_reader = reader(fo)
        for record in avro_reader:
            print(record)

def Del():
    pass