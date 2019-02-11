from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from controller.webhook import webhook_blueprint

app = Flask(__name__)
app.register_blueprint(webhook_blueprint)


@app.route("/")
def ping():
    return "Ping"


if __name__ == "__main__":
    app.run(port=5000)
