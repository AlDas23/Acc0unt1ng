from fastavro import json_reader, parse_schema

schema = {
    "name": "Standard field",
    "type": "record",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "date", "type": "string"},
        {"name": "sum", "type": "string"},
        {"name": "category", "type": "string"},
        {"name": "subcategory", "type": "string"},
        {"name": "comment", "type": "string"},
        {"name": "person_bank", "type": "string"},
        {"name": "currency", "type": "string"}
    ]
}
parsed_schema = parse_schema(schema)

keys = ["id", "date", "sum", "category", "subcategory", "comment", "person_bank", "currency"]

dbPath = ".\db\MainDB.avro"