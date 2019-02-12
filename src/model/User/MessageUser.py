from model.User.DBUser import DBUser


def make_button(title, payload):
    return {
        "type": "postback",
        "title": title,
        "payload": payload
    }


def make_quick_replies(title, payload, image_url):
    return {
        "content_type": "text",
        "title": title,
        "payload": payload,
        "image_url": image_url
    }


class MessageUser(DBUser):
    def send_text_message(self, message, quick_replies):
        self._API.send_text_message(self.messenger_id, message, quick_replies)

    def send_attachment(self, content_type, content):
        self._API.send_attachment(self.messenger_id, content_type, content)

    def send_bot_message(self, title, subtitle, buttons=None):
        element = {
            "title": title,
            "subtitle": subtitle
        }
        if buttons is not None:
            element["buttons"] = buttons
        self._API.send_generic_template(self.messenger_id, [element])

    def show_help(self):
        pass

    def show_menu(self):
        element = {
            "title": "Menu",
            "buttons": [
                make_button("Bắt đầu chat", "START_CHATTING"),
                make_button("Hướng dẫn", "HELP"),
                make_button("Đổi sở thích", "SET_FAVOURITE")
            ]
        }
        self._API.send_generic_template(self.messenger_id, [element])

    def show_end(self):
        pass

    def show_gender_list(self):
        pass
