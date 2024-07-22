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
            print(' allm - all main records\n allacc - all pb accounts\n alltran - all transfer records\n alldep - all deposit records')
            mode = input()
            print(Read(mode))
            
        elif (inp == '3'):
            print("Id of record to delete: ")
            dele = input()
            print("Type of record to delete(main/transfer): ")
            type = input()
            Del(dele, type)
            
        elif (inp == 'conf' or inp == 'Conf'):
            SpecialValues()
            
        elif (inp == 'Ndb' or inp == 'ndb'):
            print('WARNING! Might replace existing base! Y?\n')
            conf = input()
            if (conf == 'y' or conf == 'Y'):
                NewDBase()
        else:
            print('Unexpected input\n')
            
def SpecialValues():
    print("""What field values to edit?\n catinc - income category\n catexp - expense category
          \n subcat - sub-category\n curr - currency\n initpb - person_bank
           delpb - delete person_bank account\n""")
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