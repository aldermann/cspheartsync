import os
import time

from flask import request, Blueprint

from model.API import FBAPI
from model.User.User import User
from model.Cache import Cache
import logging

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
            for msg in entry["messaging"]:
                sender_id = msg["sender"]["id"]
                try:
                    postback = msg.get("postback")
                    if "message" in msg and "quick_reply" in msg["message"]:
                        postback = msg["message"]["quick_reply"]
                    if postback is not None:
                        if User.check_exist(sender_id):
                            user = User(sender_id)
                            user.process_postback(postback["payload"])
                        else:
                            user = User(sender_id, create_new=True)
                            user.show_menu()
                    else:
                        message = msg.get("message")
                        if message is not None:
                            if cache.check_in_cache(message["mid"]):
                                continue
                            cache.put(message["mid"])
                            if User.check_exist(sender_id):
                                user = User(sender_id)
                                if "text" in message:
                                    user.process_message(message["text"])
                                else:
                                    for attachment in message["attachments"]:
                                        user.process_message((attachment["type"], attachment["payload"]["url"]))
                            else:
                                user = User(sender_id, create_new=True)
                                user.show_menu()
                except Exception as e:
                    api = FBAPI()
                    key = int(time.time())
                    api.send_text_message(sender_id,
                                          "There has been an error. Please report this id: {} to admin".format(key))
                    logging.error(str(key))
                    logging.error(str(e))
                    # raise e
    return "EVENT_RECEIVED", 200
