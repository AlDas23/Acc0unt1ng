import os.path
from io import BytesIO
from fastavro import writer, reader
from db_scripts.consts import *


def Add(input_field):
    id = Read(1)  # Get the maximum ID
    if (id is None):
        id == 1
    values = input_field.split(",")
    values.insert(0, id + 1) # Change so that inserted number is +1 from biggest existing id in DB
    records = {keys[i]: values[i] for i in range(len (keys))}

    if not os.path.exists(dbPath):
        # Create file and write schema and first record
        with open(dbPath, 'wb') as out:
            writer(out, parsed_schema, [records])   
    else:
        # Append record to the existing file
        with open(dbPath, 'rb+') as out:
            out.seek(0, os.SEEK_END)  # Move to the end of the file
            writer(out, parsed_schema, [records])

def Read(x):
    if os.path.exists(dbPath): #Check if file exists
        if (x == 0): #Check who called the function. 0 for terminal, 1 for Add function
            with open(dbPath, 'rb') as fo:
                avro_reader = reader(fo)
                for record in avro_reader:
                    print(record)
        elif (x == 1):
            max_id = None
            with open(dbPath, 'rb') as fo:
                avro_reader = reader(fo)
                for record in avro_reader:
                    if max_id is None or record['id'] > max_id:
                        max_id = record['id']
            return max_id
    else:
        print("File not found.")

# def Del(del_id):
#    if os.path.exists(dbPath): #Check if file exists
    #    with open(dbPath, 'rb') as fo:
        #    avro_reader = reader(fo)
        #    for record in avro_reader:
            #    if del_id == record['id']:
                #   delete record
#    else:
    #    print("File not found.")