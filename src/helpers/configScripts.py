import toml
import os
import db_scripts.consts as consts

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


def CreateDefaultConfig():
    directory = os.path.dirname(configPath)
    if directory:
        os.makedirs(directory, exist_ok=True)

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
        LoadConfig()


def ModifyConfigLists(listType, NewList):
    if not os.path.exists(configPath):
        raise FileNotFoundError("Config file does not exist.")
    else:
        with open(configPath, "r") as cf:
            configData = toml.load(cf)

        configData["lists"][listType] = NewList

        with open(configPath, "w") as cf:
            toml.dump(configData, cf)
        print(f"Config list '{listType}' updated successfully.")
        LoadConfig()


def LoadConfig():
    if not os.path.exists(configPath):
        CreateDefaultConfig()

    with open(configPath, "r") as cf:
        configData = toml.load(cf)

        print("Config version:", configData.get("version", "N/A"))
        AssignGlobalConstants(configData)
        print("Config file loaded successfully.")
        return


def AssignGlobalConstants(configData):
    consts.mainCurrency = configData["settings"].get("main_currency", "None")
    consts.incCategories = configData["lists"].get("inc-categories", [])
    consts.expCategories = configData["lists"].get("exp-categories", [])
    consts.subCategories = configData["lists"].get("sub-categories", [])
    consts.currencies = configData["lists"].get("currencies", [])
