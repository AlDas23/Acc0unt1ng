import toml
import os
import db_scripts.consts as consts

configPath = "./config/config.toml"
currentVersion = "0.3"

defaultConfig = {
    "version": currentVersion,
    "current_year": "",
    "settings": {"main_currency": "None"},
    "lists": {
        "exp-categories": [],
        "inc-categories": [],
        "sub-categories": [],
        "currencies": [],
        "stocks": [],
    },
    "backup_years": [],
}


def UpdateConfigToNewVersion():
    if not os.path.exists(configPath):
        raise FileNotFoundError("Config file does not exist.")

    with open(configPath, "r") as cf:
        currentConfig = toml.load(cf)

    # Merge existing config with defaultConfig to ensure new fields are added
    updatedConfig = defaultConfig.copy()
    updatedConfig["settings"].update(currentConfig.get("settings", {}))
    updatedConfig["lists"].update(currentConfig.get("lists", {}))
    updatedConfig["backup_years"] = currentConfig.get("backup_years", [])
    updatedConfig["current_year"] = currentConfig.get("current_year", consts.currentYear)

    # Update the version
    updatedConfig["version"] = currentVersion

    # Save the updated configuration
    with open(configPath, "w") as cf:
        toml.dump(updatedConfig, cf)

    print("Config file updated to the new version successfully.")


def CheckVersion():
    with open(configPath, "r") as cf:
        configData = toml.load(cf)
    versionToCheck = configData.get("version", None)

    if versionToCheck != currentVersion:
        print(f"Config version mismatch: {versionToCheck} != {currentVersion}")
        UpdateConfigToNewVersion()


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
        CheckVersion()
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
        CheckVersion()
        with open(configPath, "r") as cf:
            configData = toml.load(cf)

        configData["lists"][listType] = NewList

        with open(configPath, "w") as cf:
            toml.dump(configData, cf)
        print(f"Config list '{listType}' updated successfully.")
        LoadConfig()


def AddToBackupYears(year):
    if not os.path.exists(configPath):
        raise FileNotFoundError("Config file does not exist.")
    else:
        CheckVersion()
        with open(configPath, "r") as cf:
            configData = toml.load(cf)

        if "backup_years" not in configData:
            configData["backup_years"] = []

        if year not in configData["backup_years"]:
            configData["backup_years"].append(year)
        
        configData["current_year"] = consts.currentYear

        with open(configPath, "w") as cf:
            toml.dump(configData, cf)
        print(f"Year '{year}' added to backup years successfully.")


def ReadBackupYears():
    if not os.path.exists(configPath):
        raise FileNotFoundError("Config file does not exist.")
    else:
        CheckVersion()
        with open(configPath, "r") as cf:
            configData = toml.load(cf)

        return configData.get("backup_years", [])
    
def ReadCurrentYear(year = None):
    if not os.path.exists(configPath):
        raise FileNotFoundError("Config file does not exist.")
    else:
        CheckVersion()
        with open(configPath, "r") as cf:
            configData = toml.load(cf)
            
        configYear = configData.get("current_year", "")

        if year is not None:
            return configYear == year
        else:
            return configYear

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
