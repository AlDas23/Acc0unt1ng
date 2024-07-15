from db_scripts.script import *

def Terminal():
    while (True):
        print("TERMINAL UI\n\n1. Add field\n2. Read\n3. Delete field\n")
        inp = int(input())
        if (inp == 1):
            print("Enter (Date,Sum,Category,Sub-Category,Comment,Person+bank,Currency):\n")
            field = input()
            Add(field)
        elif (inp == 2):
            Read()
        elif (inp == 3):
            Del()
        else:
            print("Unexpected input\n")