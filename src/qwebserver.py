# Its ass code - most likely hard to get it to autheficate the danging app inside the account

import os
from typing import List

import requests
from dotenv import load_dotenv
from quart import (Quart, redirect, render_template_string, request, session,
                   url_for)
from quart_oauth2_discord_py import DiscordOauth2Client, Guild
from quart_session import Session
from requests_oauthlib import OAuth2Session

load_dotenv()
TOKENBOT = os.getenv("DISCORD_TOKEN")
app = Quart(__name__)
app.secret_key = (
    b"\x92\xc2\x11\x9a\x87\xa85\t:iLjX\xd4\xe3\xbf\x9b\xf8s\x0b\xa7,\xda\xc4"
)
app.config["DISCORD_CLIENT_ID"] = "671612079106424862"
app.config["DISCORD_CLIENT_SECRET"] = "put your own"
app.config["SCOPES"] = ["identify", "guilds"]
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = TOKENBOT
token_url = "https://discord.com/api/oauth2/token"
scope = ["identify", "guilds.join"]
base_discord_api_url = "https://discord.com/api"
authorize_url = "https://discord.com/api/oauth2/authorize"
user = requests.get(base_discord_api_url + "/users/@me").json()
client = DiscordOauth2Client(app)


@app.route("/")
async def index():
    return "Guild add completed"


@app.route("/login/", methods=["GET"])
async def login():
    return await client.create_session()


@app.route("/callback")
async def callback():
    await client.callback()
    code = request.args.get("code")
    print(code)
    oauth = OAuth2Session(
        app.config["DISCORD_CLIENT_ID"], redirect_uri=app.config["DISCORD_REDIRECT_URI"]
    )
    token = oauth.fetch_token(
        token_url, client_secret=app.config["DISCORD_CLIENT_SECRET"], code=code
    )
    print(token)
    data = {
        "client_id": app.config["DISCORD_CLIENT_ID"],
        "client_secret": app.config["DISCORD_CLIENT_SECRET"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": app.config["DISCORD_REDIRECT_URI"],
    }
    headers = {
        "access_token": token,
        "Authorization": f"Bot {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    discord = make_session(state=session.get("oauth2_state"))
    url = f"{base_discord_api_url}/guilds/816985615811608616/members/{user}"
    response = requests.put(url=url, data=payload, headers=headers)
    print(response.text)
    return redirect(url_for("index"))


def return_guild_names_owner(guilds_: List[Guild]):
    # print(list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild()])))
    return list(
        sorted(
            [
                fetch_guild.name
                for fetch_guild in guilds_
                if fetch_guild.is_owner_of_guild()
            ]
        )
    )


def search_guilds_for_name(guilds_, query):
    # print(list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild() and fetch_guild.name == query])))
    return list(
        sorted(
            [
                fetch_guild.name
                for fetch_guild in guilds_
                if fetch_guild.is_owner_of_guild() and fetch_guild.name == query
            ]
        )
    )


@app.route("/guilds")
async def guilds():
    template_string = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Guilds</title>
        </head>
        <body>
            <h1>Your guilds: </h1>
            <ol>
            {% for guild_name in guild_names %}
                <li>{{ guild_name }}</li>
            {% endfor %}
            </ol>
        </body>
    </html>
    """
    if request.args.get("guild_name"):
        return await render_template_string(
            template_string,
            guild_names=search_guilds_for_name(
                await client.fetch_guilds(), request.args.get("guild_name")
            ),
        )
    return await render_template_string(
        template_string,
        guild_names=return_guild_names_owner(await client.fetch_guilds()),
    )


@app.route("/me")
@client.is_logged_in
async def me():
    user = await client.fetch_user()
    image = user.avatar_url
    # noinspection HtmlUnknownTarget
    return await render_template_string(
        """
        <html lang="en">
            <body>
                <p>Login Successful</p>
                <img src="{{ image_url }}" alt="Avatar url">
            </body>
        </html>
        """,
        image_url=image,
    )


if __name__ == "__main__":
    app.run()
