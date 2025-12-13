from api.api_run import app
from db_scripts import consts
from db_scripts.dbScripts import UpdateDBYear
from helpers.configScripts import LoadConfig, ReadCurrentYear
from helpers.extras import GetCurrentYear

if __name__ == "__main__":
    consts.currentYear = GetCurrentYear()
    LoadConfig()
    if (not ReadCurrentYear(consts.currentYear)):
        UpdateDBYear()
    app.run(host="0.0.0.0", debug=True, port=5050)
