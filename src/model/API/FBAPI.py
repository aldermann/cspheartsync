import os
import urllib.parse as urlparser
import const.postback_name as postback
import requests

from model.API import APIInterface


class FBAPI(APIInterface):
    __access_token = os.getenv("ACCESS_TOKEN")

    def get_url(self, api_path):
        api_path = os.path.normpath("/".join(["/v3.2", api_path]))
        url = urlparser.urljoin("https://graph.facebook.com", api_path)
        url_parts = list(urlparser.urlparse(url))
        query = urlparser.parse_qs(url_parts[4])
        query["access_token"] = self.__access_token
        url_parts[4] = urlparser.urlencode(query)
        return urlparser.urlunparse(url_parts)

    def send(self, recipient_id, payload):
        url = self.get_url("/me/messages")
        data = {
            "messaging_type": "RESPONSE",
            "recipient": {
                "id": str(recipient_id)
            },
            "message": payload
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(response.text, data)
        return response.json()

    def get_user_data(self, messenger_id):
        url = self.get_url("/{}?fields=first_name,last_name,profile_pic,gender".format(messenger_id))
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def send_text_message(self, recipient, message, quick_replies=None):
        data = {
            "text": message
        }
        if quick_replies is not None:
            if not isinstance(quick_replies, list):
                quick_replies = [quick_replies]
            data["quick_replies"] = quick_replies
        return self.send(recipient, data)

    def send_attachment(self, recipient, content_type, content, quick_replies=None):
        data = {
            "attachment": {
                "type": content_type,
                "payload": {
                    "url": content,
                    "is_reusable": True
                }
            }
        }
        if quick_replies is not None:
            if not isinstance(quick_replies, list):
                quick_replies = [quick_replies]
            data["quick_replies"] = quick_replies
        return self.send(recipient, data)

    def send_generic_template(self, recipient, elements, quick_replies=None):
        data = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
        if quick_replies is not None:
            if not isinstance(quick_replies, list):
                quick_replies = [quick_replies]
            data["quick_replies"] = quick_replies
        return self.send(recipient, data)

    def setup_getstarted(self):
        url = self.get_url("/me/messenger_profile")
        data = {
            "get_started": {
                "payload": postback.get_started
            },
            "persistent_menu": [
                {
                    "locale": "default",
                    "composer_input_disabled": False,
                    "call_to_actions": [
                        {
                            "type": "postback",
                            "title": "End Chat",
                            "payload": postback.request_stop_chatting
                        }
                    ]
                }
            ]

        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(response.text)
