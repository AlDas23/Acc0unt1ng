from db_scripts.script import *

def Terminal():
    while (True):
        print("""TERMINAL UI\n\n1. Add field\n2. Read\n3. Delete field\nConf. Configure special field values\nNdb. New DataBase\n""")
        inp = input()
        
        if (inp == '1'):
            print('Mode?\n m - main\n t - transfer\n d - deposit')
            mode = input()
            if (mode == 'm'):
                print("Enter (Date,Category,Sub-Category,Person+bank,Comment,Sum,Currency):\n")
                field = input()
                mode = 'main'
            elif (mode == 't'):
                print("Enter (Date,Sender,Reciever,Comment,Sum,Currency):\n")
                field = input()
                mode = 'transfer'
            elif (mode == 'd'):
                print("Enter (Date_in,name,comment,sum,currency,months,date_out,percent,currency_rate):\n")
                field = input()
                mode = 'deposit'
            Add(field, mode)
            
        elif (inp == '2'):
            print(""" 
                 allm - all main records
                 allacc - all pb accounts
                 m+ - positive main records
                 m- - negative main records
                 allcurr - all currencies
                 alltran - all transfer records
                 alladvtran - all advanced transfer records
                 alldep - all deposit records
                 alldepacc - deposit accounts
                 opendep - open deposits
                 closeddep - closed deposits
                 """)
            mode = input()
            print(Read(mode))
            
        elif (inp == '3'):
            print("Id of record to delete: ")
            dele = input()
            print("Type of record to delete(main/transfer): ")
            type = input()
            Del(dele, type)
            
        elif (inp == 'conf' or inp == 'Conf'):
            print(" spv - special values\n mark - markers\n")
            inp = input()
            if (inp == 'spv'):
                SpecialValues()
            elif (inp == 'mark'):
                PreMark()
            
        elif (inp == 'Ndb' or inp == 'ndb'):
            print('WARNING! Might replace existing base! Y?\n')
            conf = input()
            if (conf == 'y' or conf == 'Y'):
                NewDBase()
        else:
            print('Unexpected input\n')
            
def PreMark():
    print("Existing type markers:\n", Read('extype'), "\n")
    print("Existing owner markers:\n", Read('exowner'), "\n\n")
    print("owner or type marker?: ")
    select = input()
    if (select == 'type'):
        print("Input new marker (person_bank,type)\n")
        input_field = input()
        Mark(input_field, select)
        
    elif (select == 'owner'):
        print("Input new marker (person_bank,owner)\n")
        input_field = input()
        Mark(input_field, select)
            
def SpecialValues():
    print("""
        What field values to edit?
         catinc - income category
         catexp - expense category
         subcat - sub-category
         curr - currency
         initpb - person_bank
         delpb - delete person_bank account
        """)
    inp = input()
    if (inp == 'catinc'):
        SPVconf(inp)
    elif (inp == 'catexp'):
        SPVconf(inp)
    elif (inp == 'subcat'):
        SPVconf(inp)
    elif (inp == 'curr'):
        SPVconf(inp)
    elif (inp == 'initpb'):
        InitPB()
    elif (inp == 'delpb'):
        DelPB()
    else:
        print("Unknown command!\n\n")