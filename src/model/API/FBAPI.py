import os
import urllib.parse as urlparser

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

    def send_message(self, recipient_id, payload):
        url = self.get_url("/me/messages")
        data = {
            "messaging_type": "RESPONSE",
            "recipient": {
                "id": str(recipient_id)
            },
            "message": payload
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_user_data(self, messenger_id):
        url = self.get_url("/{}?fields=first_name,last_name,profile_pic,gender".format(messenger_id))
        response = requests.get(url)
        return response.json()

    def send_text_message(self, recipient, message):
        return self.send_message(recipient, {
            "text": message
        })

    def send_attachment(self, recipient, content_type, content):
        return self.send_message(recipient, {
            "attachment": {
                "type": content_type,
                "payload": {
                    "url": content,
                    "is_reusable": True
                }
            }
        })
