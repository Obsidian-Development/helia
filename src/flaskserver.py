# Flask web server - launch as web app in heroku
import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, Unauthorized, requires_authorization

app = Flask(__name__)

load_dotenv()
TOKENBOT = os.getenv("DISCORD_TOKEN")

app.secret_key = b"random bytes representing flask secret key"
# !! Only in development environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = 671612079106424862  # Discord client ID.
# Discord client secret.
app.config["DISCORD_CLIENT_SECRET"] = "put your own"
# URL to your callback endpoint.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
# Required to access BOT resources.
app.config["DISCORD_BOT_TOKEN"] = TOKENBOT

discordoauth = DiscordOAuth2Session(app)


@app.route("/")
async def index():
    return "Guild add completed"


@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discordoauth.callback()
    code = request.args.get("code")
    print(code)
    print(token)
    url = f"{base_discord_api_url}/guilds/816985615811608616/members/{user}"
    response = requests.put(url=url, data=payload, headers=headers)
    print(response.text)
    return redirect(url_for("index"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""


if __name__ == "__main__":
    app.run()
