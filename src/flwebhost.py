from threading import Thread

from flask import Flask
from flask import render_template

app = Flask("")


@app.route("/")
def main():
    return render_template("404.html")


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()
