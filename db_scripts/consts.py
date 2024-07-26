dbPath = '.\db\Main.db'
SPVcatIncPath = '.\db\catInc.csv'
SPVcatExpPath = '.\db\catExp.csv'
SPVsubcatPath = '.\db\subcat.csv'
SPVcurrPath = '.\db\curr.csv'

keys = ["id", "date", "category", "sub_category", "person_bank", "comment", "sum", "currency"]
tr_keys = ["id", "date", "person_bank_from", "person_bank_to", "comment" ,"sum", "currency"]
advtr_keys = ["id", "date", "person_bank_from", "sum_from", "currency_from", "person_bank_to", "sum_to", "currency_to",  "comment"]
dp_keys = ["date_in", "name", "owner", "comment", "sum", "currency", "months" ,"date_out", "percent", "currency_rate", "expect"]