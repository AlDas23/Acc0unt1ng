import toml
import os
from src.db_scripts.consts import (
    mainCurrency,
    incCategories,
    expCategories,
    subCategories,
    currencies,
)

configPath = "./config/config.toml"

defaultConfig = {
    "version": "0.1",
    "settings": {"main_currency": "None"},
    "lists": {
        "exp-categories": [],
        "inc-categories": [],
        "sub-categories": [],
        "currencies": [],
    },
}


def CreateConfig():
    if not os.path.exists(configPath):
        with open(configPath, "w") as cf:
            toml.dump(defaultConfig, cf)
        print("Config file created with default settings.")
    else:
        raise FileExistsError("Config file already exists.")


def ModifyConfigSettings(param, value):
    if not os.path.exists(configPath):
        raise FileNotFoundError("Config file does not exist.")
    else:
        with open(configPath, "r") as cf:
            configData = toml.load(cf)

        configData["settings"][param] = value

        with open(configPath, "w") as cf:
            toml.dump(configData, cf)
        print(f"Config setting '{param}' updated successfully.")
        return


def ModifyConfigLists(NewList, listType):
    if not os.path.exists(configPath):
        raise FileNotFoundError("Config file does not exist.")
    else:
        with open(configPath, "r") as cf:
            configData = toml.load(cf)

        configData["lists"][listType] = NewList

        with open(configPath, "w") as cf:
            toml.dump(configData, cf)
        print(f"Config list '{listType}' updated successfully.")
        return


def LoadConfig():
    if not os.path.exists(configPath):
        raise FileNotFoundError("Config file does not exist.")
    else:
        with open(configPath, "r") as cf:
            configData = toml.load(cf)

        print("Config version:", configData.get("version", "N/A"))
        AssignGlobalConstants(configData)
        print("Config file loaded successfully.")
        return


def AssignGlobalConstants(configData):
    global mainCurrency, incCategories, expCategories, subCategories, currencies

    mainCurrency = configData["settings"].get("main_currency", "None")
    incCategories = configData["lists"].get("inc-categories", [])
    expCategories = configData["lists"].get("exp-categories", [])
    subCategories = configData["lists"].get("sub-categories", [])
    currencies = configData["lists"].get("currencies", [])
