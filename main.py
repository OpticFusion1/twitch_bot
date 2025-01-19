import json
from flask import Flask
from auth import BotAuth

def main():
    # Load the config from the config.json file
    with open('config.json') as f:
        config = json.load(f)

    # Extract the necessary values from the config file
    client_id = config['twitch_client_id']
    twitch_secret = config['twitch_secret']
    session_secret = config['session_secret']
    callback_url = config['callback_url']

    # Initialize Flask app first
    app = Flask(__name__)

    # Create an instance of BotAuth and pass the app and config
    auth = BotAuth(app, client_id, twitch_secret, session_secret, callback_url)

    # Run the app
    app.run(port=5000)

if __name__ == "__main__":
    main()