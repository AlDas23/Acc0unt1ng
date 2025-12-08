dbPath = "./db/Main.db"
SPVcatIncPath = "./db/catInc.csv"
SPVcatExpPath = "./db/catExp.csv"
SPVsubcatPath = "./db/subcat.csv"
SPVcurrPath = "./db/curr.csv"
SPVstockPath = "./db/stock.csv"

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
curr_keys_legacy = ["date", "currency", "rate"]
curr_keys = ["date", "currency_M", "currency_S", "rate"]

expected_tables = {
    "main": [
        "id",
        "date",
        "category",
        "sub_category",
        "person_bank",
        "sum",
        "currency",
        "comment",
    ],
    "exc_rate": ["id", "date", "currency_M", "currency_S", "rate"],
    "deposit": [
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
    ],
    "transfer": [
        "id",
        "date",
        "person_bank_from",
        "person_bank_to",
        "sum",
        "currency",
        "comment",
    ],
    "advtransfer": [
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
    ],
    "Init_PB": ["person_bank", "sum", "currency"],
    "Marker_owner": ["bank_rec", "owner"],
    "Marker_type": ["bank_rec", "type"],
    "investTransaction": [
        "id",
        "date",
        "PB",
        "amount",
        "currency",
        "investPB",
        "investAmount",
        "stock",
        "fee",
    ],
    "investPB": ["name", "stock"],
    "investStockPrice": ["id", "date", "stock", "price"],
}

old_tables = {
    "exc_rate": ["date", "currency", "rate"],
}

currentYear = None

isLegacyCurrencyRates = False

mainCurrency = None

incCategories = []
expCategories = []
subCategories = []
currencies = []
