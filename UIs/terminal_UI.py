from db_scripts.script import *

def Terminal():
    while (True):
        print("TERMINAL UI\n\n1. Add field\n2. Read\n3!!. Delete field\n")
        inp = int(input())
        if (inp == 1):
            print("Enter (Date,Sum,Category,Sub-Category,Comment,Person+bank,Currency):\n")
            field = input()
            Add(field)
        elif (inp == 2):
            Read(0)
        # elif (inp == 3):
            # print("Id of record to delete: ")
            # dele = int(input())
            # Del(dele)
        else:
            print("Unexpected input\n")