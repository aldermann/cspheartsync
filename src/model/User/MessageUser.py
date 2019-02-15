from model.User.DBUser import DBUser
import const.postback_name as postback_name


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
    def send_text_message(self, message, quick_replies=None):
        self._API.send_text_message(self.messenger_id, message, quick_replies)

    def send_attachment(self, content_type, content, quick_replies=None):
        self._API.send_attachment(self.messenger_id, content_type, content, quick_replies)

    def send_bot_message(self, title, subtitle, buttons=None, quick_replies=None):
        element = {
            "title": title,
            "subtitle": subtitle
        }
        if buttons is not None:
            if not isinstance(buttons, list):
                buttons = [buttons]
            element["buttons"] = buttons
        self._API.send_generic_template(self.messenger_id, [element], quick_replies=quick_replies)

    def show_help(self):
        pass

    def show_menu(self):
        element = {
            "title": "Menu",
            "buttons": [
                make_button("Bắt đầu chat", postback_name.start_chatting),
                make_button("Hướng dẫn", postback_name.get_help),
                make_button("Đổi sở thích", postback_name.set_favourite)
            ]
        }
        self._API.send_generic_template(self.messenger_id, [element])

    def show_end(self):
        qr = [make_quick_replies("Có", postback_name.stop_chatting,
                                 "https://xn--i-7iq.ws/emoji-image/%E2%9C%94%EF%B8%8F.png?format=ios")]
        self.send_bot_message("Dừng trò chuyện", "Bạn có chắc chắn không?",
                              quick_replies=qr)

    def show_gender_list(self):
        qr = [make_quick_replies("Nam", postback_name.favour_male,
                                 "https://xn--i-7iq.ws/emoji-image/%F0%9F%91%A6.png?format=ios"),
              make_quick_replies("Nữ", postback_name.favour_female,
                                 "https://xn--i-7iq.ws/emoji-image/%F0%9F%91%A7.png?format=ios"),
              make_quick_replies("Ai cũng được", postback_name.favour_any,
                                 "https://xn--i-7iq.ws/emoji-image/%F0%9F%91%AB.png?format=ios")]
        self.send_bot_message("Chọn sở thích", "Bạn muốn được ghép cặp với giới tính nào?",
                              quick_replies=qr)

    # send while in queue
    def start_queuing(self):
        self.send_bot_message("Tìm cặp", "Hãy đợi một chút để bot tìm cặp cho bạn",
                              make_button("Hủy", postback_name.cancel_queuing))

    def still_queuing(self):
        self.send_bot_message("Hãy chờ đợi", "Chúng tôi đang tìm kiếm cho bạn người trò chuyện",
                              make_button("Hủy", postback_name.cancel_queuing))

    def stop_queuing(self):
        self.send_bot_message("Hủy tìm kiếm", "Bạn đã hủy việc tìm kiếm người trò chuyện")
        self.show_menu()

    def start_chatting(self):
        self.send_bot_message("Đã ghép cặp", "Hãy bắt đầu cuộc trò chuyện của bạn")

    def stop_chatting(self, is_stopper):
        if is_stopper:
            self.send_bot_message("Kết thúc", "Bạn đã kết thúc cuộc trò chuyện")
        else:
            self.send_bot_message("Kết thúc", "Cuộc trò chuyện đã kết thúc")
