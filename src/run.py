import os
from pyngrok import ngrok
from api.api_run import app

if __name__ == "__main__":
    ngrok_authtoken = os.getenv("NGROK_AUTHTOKEN")

    if ngrok_authtoken:
        # Authenticate Ngrok
        ngrok.set_auth_token(ngrok_authtoken)

    # Open a tunnel on the default port 5000
    public_url = ngrok.connect(5000)
    print(f" * Ngrok tunnel available at: {public_url}")

    # Start the Flask app
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600
    app.run()
