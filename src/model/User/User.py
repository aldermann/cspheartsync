import const.postback_name as postback_name
import const.context_name as context_name
from model.User.MessageUser import MessageUser
import time

class User(MessageUser):
    def __init__(self, user_messenger_id, create_new=False):
        if create_new:
            super().__init__(user_messenger_id, False)
            self._fetch_user_data_from_facebook()
            self._insert_user()
            self.send_bot_message("Chào mừng", "Chào mừng bạn đã đến với CSP Heartsync. Nhớ xem hướng dẫn nhé")
        super().__init__(user_messenger_id)

    def pair(self):
        partner_id = User._lookup(self.gender, self.favourite)
        if partner_id is None:
            self.bot_context = context_name.queuing
            self.enqueue_time = time.time()
            self.save()
            self.start_queuing()
        else:
            self.partner = partner_id
            self.bot_context = context_name.chatting
            self.enqueue_time = None;
            self.start_chatting()
            self.save()
            partner = User(partner_id)
            partner.partner = self.messenger_id
            partner.bot_context = context_name.chatting
            partner.enqueue_time = None;
            partner.start_chatting()
            partner.save()

    def unpair(self):
        partner = User(self.partner)
        partner.partner = None
        partner.bot_context = context_name.home
        partner.stop_chatting(False)
        partner.show_menu()
        partner.save()
        self.partner = None
        self.bot_context = context_name.home
        self.stop_chatting(True)
        self.show_menu()
        self.save()

    def forward_text_message(self, message):
        partner = User(self.partner)
        partner.send_text_message(message)

    def forward_attachment(self, content_type, content):
        partner = User(self.partner)
        partner.send_attachment(content_type, content)

    def process_message(self, message):
        if self.bot_context == context_name.home:
            self.pair()
        elif self.bot_context == context_name.chatting:
            if isinstance(message, tuple):
                self.forward_attachment(message[0], message[1])
            else:
                if message.lower() == "end chat":
                    self.show_end()
                if message.lower() == "just end chat":
                    self.unpair()
                else:
                    self.forward_text_message(message)
        elif self.bot_context == context_name.queuing:
            if message == "cancel":
                self.bot_context = context_name.home
                self.stop_queuing()
                self.save()
            else:
                self.still_queuing()

    def process_postback(self, postback):
        print(postback)
        if postback == postback_name.get_started:
            self.bot_context = context_name.home
            self.show_menu()
            self.save()

        elif postback == postback_name.get_help:
            self.show_help()

        elif self.bot_context == context_name.home:
            if postback == postback_name.show_menu:
                self.show_menu()
            elif postback == postback_name.start_chatting:
                self.pair()
            elif postback == postback_name.set_favourite:
                self.show_gender_list()
            elif postback[0:7] == "FAVOUR_":
                self.favourite = postback[7:].lower()
                self.changed_favourite(self.favourite)
                self.show_menu()
                self.save()
            else:
                self.show_help()

        elif self.bot_context == context_name.chatting:
            if postback == postback_name.stop_chatting:
                self.unpair()
            elif postback == postback_name.request_stop_chatting:
                self.show_end()
            else:
                self.send_bot_message("Không phải bây giờ", "Hãy cài đặt sau khi kết thúc cuộc trò chuyện")

        elif self.bot_context == context_name.queuing:
            if postback == postback_name.cancel_queuing or postback == postback_name.request_stop_chatting:
                self.bot_context = context_name.home
                self.stop_queuing()
                self.save()
            else:
                self.send_bot_message("Không phải bây giờ", "Hãy cài đặt sau khi rời khỏi hàng đợi")
