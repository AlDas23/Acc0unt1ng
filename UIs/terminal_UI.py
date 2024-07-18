from db_scripts.script import *

def Terminal():
    while (True):
        print("TERMINAL UI\n\n1. Add field\n2. Read\n3. Delete field\nNdb. New DataBase\n")
        inp = input()
        if (inp == '1'):
            print('Mode?\n m - main\n t - transfer\n')
            mode = input()
            if (mode == 'm'):
                print("Enter (Date,Category,Sub-Category,Person+bank,Comment,Sum,Currency):\n")
                field = input()
                mode = 'main'
            elif (mode == 't'):
                print("Enter (Date,Sender,Reciever,Comment,Sum,Currency):\n")
                field = input()
                mode = 'transfer'
            Add(field, mode)
        elif (inp == '2'):
            print(' allm - all main records\n allacc - all pb accounts\n alltran - all transfer records')
            mode = input()
            Read(mode)
        elif (inp == '3'):
            print("Id of record to delete: ")
            dele = input()
            Del(dele)
        elif (inp == 'Ndb' or inp == 'ndb'):
            print('WARNING! Might replace existing base! Y?\n')
            conf = input()
            if (conf == 'y' or conf == 'Y'):
                NewDBase()
        else:
            print('Unexpected input\n')