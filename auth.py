import requests
import asyncio
from flask import Flask, render_template_string, request
from flask_oauthlib.client import OAuth
from bot import Bot

# TODO: Implement better pages
class BotAuth:
    def __init__(self, app, client_id, twitch_secret, session_secret, callback_url):
        self.app = app
        self.twitch_secret = twitch_secret
        self.client_id = client_id
        self.callback_url = callback_url
        self.session_secret = session_secret

        self.access_token = None

        self.oauth = OAuth(self.app)
        self.twitch = self.oauth.remote_app(
            'twitch',
            consumer_key=self.client_id,
            consumer_secret=self.twitch_secret,

            # TODO: Make the scopes configurable
            request_token_params={
                'scope': 'channel:manage:broadcast'
            },
            base_url='https://api.twitch.tv/helix/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='https://id.twitch.tv/oauth2/token',
            authorize_url='https://id.twitch.tv/oauth2/authorize',
        )

        @self.twitch.tokengetter
        def get_twitch_token():
            # Return the access token and token type
            return self.access_token, 'Bearer'

        # Set app config
        self.app.config['CLIENT_ID'] = self.client_id
        self.app.config['CALLBACK_URL'] = self.callback_url
        self.app.config['SESSION_SECRET'] = self.session_secret
        self.app.secret_key = self.session_secret
        self.app.debug = True

        # Register routes
        self.register_routes()

    def register_routes(self):
        @self.app.route("/start_bot")
        def start_bot():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            bot = Bot(self.access_token)
            bot.run()
            return render_template_string("Bot is running");

        @self.app.route('/auth/twitch/callback')
        def oauth_callback():
            # Get the authorization code from the callback
            code = request.args.get('code')

            # Exchange the code for an access token using requests
            token_url = 'https://id.twitch.tv/oauth2/token'
            data = {
                'client_id': self.client_id,
                'client_secret': self.twitch_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.callback_url,
            }
            response = requests.post(token_url, data=data)

            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')

                print(self.access_token)

                if self.access_token:
                    return render_template_string("Authentication successful!")
                else:
                    return render_template_string("Failed to retrieve access token.")
            else:
                return render_template_string(f"Error: {response.status_code}, {response.text}")

        @self.app.route('/')
        def index():
            # TODO: Make the scope configurable
            return render_template_string(f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={self.client_id}&redirect_uri={self.callback_url}&scope=chat:read+chat:edit+channel:manage:broadcast&state={self.session_secret}")