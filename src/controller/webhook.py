import os
from flask import request, Blueprint
from model.User.User import User
from model.Cache import Cache

webhook_blueprint = Blueprint("webhook", __name__)
cache = Cache()


@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook():
    webhook_token = os.getenv("WEBHOOK_TOKEN")
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == webhook_token:
        return challenge
    else:
        return "", 403


@webhook_blueprint.route("/webhook", methods=["POST"])
def webhook_post():
    body = request.get_json()
    if body["object"] == "page":
        for entry in body["entry"]:
            msg = entry["messaging"][0]
            sender_id = msg["sender"]["id"]
            message = msg.get("message")
            if message is not None:
                if cache.check_in_cache(message["mid"]):
                    continue
                cache.put(message["mid"])
                if User.check_exist(sender_id):
                    user = User(sender_id)
                    user.process_message(message["text"])
                else:
                    user = User(sender_id, create_new=True)
                    user.send_text_message("You're new. Welcome")
    return "EVENT_RECEIVED", 200
