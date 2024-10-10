# Acc0unt1ng

A python based project for managing accounting.

## Getting started 

# Local version

Instal Python from https://www.python.org/downloads/. <br>
In projects folder, run setup.bat **only ONCE**. <br>

Firts time you will need to setup categories, currencies and accounts through Terminal UI.

To start Acc0unt1ng app, run Start-user.bat, after local server starts, in console will appear line:

```
Running on http://XXX.X.X.X:XXXX
```

Open this url in your preffered browser.

# Colab version

To use colab version go to "colab" branch of this repository.


## Extras

### Startup arguments

All parameters go into `set PARAMS=` in *Start-user.bat*.

* --terminal - Runs app with Terminal UI

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

If using Postman, send "raw" POST requests for program to work correctly.
