from api.api_run import app
from src.helpers.configScripts import LoadConfig

if __name__ == "__main__":
    LoadConfig()
    app.run(host="0.0.0.0", debug=True, port=5050)
