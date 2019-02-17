from flask import Flask
from dotenv import load_dotenv
import sys
import logging

load_dotenv()

from model.API.FBAPI import FBAPI
from controller.webhook import webhook_blueprint

if len(sys.argv) >= 2 and sys.argv[1] == "setup":
    API = FBAPI()
    API.setup_getstarted()
    exit(0)
app = Flask(__name__)
app.register_blueprint(webhook_blueprint)


@app.route("/")
def ping():
    return "Ping"


if __name__ == "__main__":
    app.run(port=5000)
