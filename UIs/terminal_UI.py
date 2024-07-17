from db_scripts.script import *

def Terminal():
    while (True):
        print("TERMINAL UI\n\n1. Add field\n2. Read\n3!!. Delete field\nNdb. New DataBase\n")
        inp = input()
        if (inp == '1'):
            print("Enter (Date,Sum,Category,Sub-Category,Comment,Person+bank,Currency):\n")
            field = input()
            Add(field)
        elif (inp == '2'):
            Read()
        elif (inp == '3'):
            print("Id of record to delete: ")
            dele = input()
            #Del(dele)
        elif (inp == 'Ndb' or inp == 'ndb'):
            print("WARNING! Might replace existing base!\n")
            conf = input()
            if (conf == 'y' or conf == 'Y'):
                NewDBase()
        else:
            print("Unexpected input\n")