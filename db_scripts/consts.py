dbPath = ".\db\Main.db"
SPVcatIncPath = ".\db\catInc.csv"
SPVcatExpPath = ".\db\catExp.csv"
SPVsubcatPath = ".\db\subcat.csv"
SPVcurrPath = ".\db\curr.csv"
SPVstockPath = ".\db\stock.csv"

keys = [
    "date",
    "category",
    "sub_category",
    "person_bank",
    "sum",
    "currency",
    "comment",
]
tr_keys = [
    "id",
    "date",
    "person_bank_from",
    "person_bank_to",
    "sum",
    "currency",
    "comment",
]
advtr_keys = [
    "id",
    "date",
    "person_bank_from",
    "sum_from",
    "currency_from",
    "person_bank_to",
    "sum_to",
    "currency_to",
    "currency_rate",
    "comment",
]
dp_keys = [
    "date_in",
    "name",
    "owner",
    "sum",
    "currency",
    "months",
    "date_out",
    "percent",
    "currency_rate",
    "expect",
    "comment",
    "isOpen",
]
curr_keys = ["date", "RON", "UAH", "EUR", "USD", "GBP", "CHF", "HUF", "AUR"]
