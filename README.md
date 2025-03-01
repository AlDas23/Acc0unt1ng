# Acc0unt1ng

A python based project for managing accounting.

## Getting started 

Run notebook from <a target="_blank" href="https://colab.research.google.com/github/AlDas23/Acc0unt1ng/blob/colab/Acc0unt1ng.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a> <br>
Run Setup cell after acquiring cloud machine (always). <br>
Paste your ngrok authtoken into "ngrok_authtoken" field and run webui. If you want notebook to remember that authtoken, after pasting it into the field, you will need to save that notebook as your own copy.<br>

### Synchronizing DB changes over multiple users

To be able to modify DB from other accounts, you will need to run Acc0unt1ng at least once. That will make a **Acc0unt1ng** folder in your Google drive. Share entire folder with users you want to give access to. Then they should find that shared folder and add a shortcut to shared folder in the root of their's drive.

## Initial setup requirements

After installing requirements using Colab cell, you will need to add some parameters regarding currencies and categories for app to work (Only once). 

There are 4 .csv files that need to be initialized/placed into the *Acc0unt1ng* folder on your drive.

![dbPreview](preview/dbPreview.png)

Each of them should have next structure: 

![csvStructure](preview/csvStructure.png)

Each currency/category/sub-category name is written on the new line
and the last row should **should not** be empty line, otherwise it would count as additional variable name.

If you would prefer to not create those files but let the app do it for you, it is possible to configure all of those csv's using *Terminal UI* cell.

![terminalSPVPreview](preview/terminalSPVPreview.png)

Under *Conf -> spv* menu you can select which values to edit.

## Account creation and marking

To create account, you will need to use either *TerminalUI* to add record of desired account and then mark it with appropriate *type* and *owner* signals, or using API requests when WebUI is running (WebUI can run even if no accounts were created).

### Using TerminalUI:

![initpbPreview](preview/initpbPreview.png)

Console instructions will guide you to the excpected format of the account record. <br> To clarify, all accounts in the Acc0unt1ng are called *person_bank* for easier understanding of ***"which account is whose?"***, but this is no hard requirement.

After creating *person_bank* record, it is needed to mark it with *type* and *owner* signals. Under *conf -> spv -> mark* menu, you can look over existing markings of *type* and *owner* and also modify them.

For example, *person_bank* called "JohnDoe credit1", can be marked as "Credit" *type* to show that this is credit card account, and with "John" *owner* to show that owner of the account is John.

### Using API requests

By sending GET request to the */api/conf/spv* you will get response of how should POST request look for account to be created, or to the */api/conf/mark* to mark existing accounts. <br> All rules for creating accounts and markings are same as the rules when creating them in TerminalUI.

# Extras

### API navigation

When running Acc0unt1ng in webUI mode, it is possible to use special API commands to gain most functionality of Terminal UI, but while running webUI.

To access API, send a GET request at */api* or */api/help*.
You will recieve navigation help that copies most of the Terminal UI functionality.

How response looks:

```
API - Help message:

Go to /api/read for Read functions.
Go to /api/conf/mark to configure Markers.
Go to /api/conf/spv to configure SPVs and account initialization function.
Go to /api/conf/spv/read to read existing SPVs.
```

Each of the paths have GET response for instruction and POST for reading, changing, deleting functions.

If using Postman, send *form-data* POST requests for program to work correctly.