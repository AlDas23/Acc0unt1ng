# Acc0unt1ng

A python based project for managing accounting.

## Getting started

### Local version

Instal Python from <https://www.python.org/downloads/>.

In projects folder, run setup.bat **only ONCE**.

To start Acc0unt1ng app, run Start-user.bat, after local server starts, this will appear in the console window:

```bash
Running on http://XXX.X.X.X:XXXX
```

Open this link in your preffered browser and enjoy Acc0unt1ng.

### Colab version

To use colab version go to "colab" branch of this repository.

## Initial setup requirements

After installing requirements using either setup.bat or Colab cell, you will need to add some parameters regarding currencies and categories for app to work (Only once).

There are 4 .csv files that need to be initialized/placed into the *db* folder of the project.
![dbPreview](preview/dbPreview.png)
Each of them should have next structure:

![csvStructure](preview/csvStructure.png)

Each currency/category/sub-category name is written on the new line
and the last row should **should not** be empty line, otherwise it would count as additional variable name.

If you would prefer to not create those files but let the app do it for you, it is possible to configure all of those csv's using *Terminal UI*.

![terminalSPVPreview](preview/terminalSPVPreview.png)

Under *Conf -> spv* menu you can select which values to edit.

## Account creation and marking

To create account, you will need to use either *TerminalUI* to add record of desired account and then mark it with appropriate *type* and *owner* signals, or using API requests when WebUI is running (WebUI can run even if no accounts were created).

### Using TerminalUI

![initpbPreview](preview/initpbPreview.png)

Console instructions will guide you to the excpected format of the account record.

To clarify, all accounts in the Acc0unt1ng are called *person_bank* for easier understanding of ***"which account is whose?"***, but this is no hard requirement.

After creating *person_bank* record, it is needed to mark it with *type* and *owner* signals. Under *conf -> spv -> mark* menu, you can look over existing markings of *type* and *owner* and also modify them.

For example, *person_bank* called "JohnDoe credit1", can be marked as "Credit" *type* to show that this is credit card account, and with "John" *owner* to show that owner of the account is John.

## Extras

### Startup arguments

All parameters go into `set PARAMS=` in *Start-user.bat*. Leaving it empty means running default configuration - using WebUI.

* --terminal - Runs app with Terminal UI
