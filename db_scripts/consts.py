dbPath = "/content/drive/MyDrive/Acc0unt1ng/Main.db"
SPVcatIncPath = "/content/drive/MyDrive/Acc0unt1ng/catInc.csv"
SPVcatExpPath = "/content/drive/MyDrive/Acc0unt1ng/catExp.csv"
SPVsubcatPath = "/content/drive/MyDrive/Acc0unt1ng/subcat.csv"
SPVcurrPath = "/content/drive/MyDrive/Acc0unt1ng/curr.csv"

keys = [
    "id",
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
