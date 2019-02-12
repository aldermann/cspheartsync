from model.User.MessageUser import MessageUser, make_quick_replies


class User(MessageUser):
    def __init__(self, user_messenger_id, create_new=False):
        if create_new:
            super().__init__(user_messenger_id, False)
            self.fetch_user_data()
            self._insert_user()
        super().__init__(user_messenger_id)

    def pair(self):
        partner_id = User.lookup()
        if partner_id is None:
            self.bot_context = "queuing"
            self.save()
            self.send_bot_message("Tìm cặp", "Hãy đợi một chút để bot tìm cặp cho bạn")
        else:
            self.partner = partner_id
            self.bot_context = "chatting"
            self.send_bot_message("Đã ghép cặp", "Hãy bắt đầu cuộc trò chuyện của bạn")
            self.save()
            partner = User(partner_id)
            partner.partner = self.messenger_id
            partner.bot_context = "chatting"
            partner.send_bot_message("Đã ghép cặp", "Hãy bắt đầu cuộc trò chuyện của bạn")
            partner.save()

    def unpair(self):
        partner = User(self.partner)
        partner.partner = None
        partner.bot_context = "home"
        partner.send_bot_message("Kết thúc", "Cuộc trò chuyện đã kết thúc")
        partner.show_menu()
        partner.save()
        self.partner = None
        self.bot_context = "home"
        self.send_bot_message("Kết thúc", "Bạn đã kết thúc cuộc trò chuyện")
        self.show_menu()
        self.save()

    def forward_text_message(self, message):
        partner = User(self.partner)
        partner.send_text_message(message)

    def forward_attachment(self, content_type, content):
        partner = User(self.partner)
        partner.send_attachment(content_type, content)

    def process_message(self, message):
        if self.bot_context == "home":
            self.pair()
        elif self.bot_context == "chatting":
            if message == "end_chat":
                self.unpair()
            else:
                if isinstance(message, tuple):
                    self.forward_attachment(message[0], message[1])
                self.forward_text_message(message)
        elif self.bot_context == "queuing":
            if message == "cancel":
                self.bot_context = "home"
                self.send_bot_message("Hủy tìm kiếm", "Bạn đã hủy việc tìm kiếm người trò chuyện")
                self.show_menu()
                self.save()
            else:
                self.send_bot_message("Hãy chờ đợi", "Chúng tôi đang tìm kiếm cho bạn người trò chuyện")

    def process_postback(self, postback):
        if self.bot_context == "home":
            if postback == "START_CHATTING":
                self.pair()
            elif postback == "HELP":
                self.show_help()
            elif postback == "SET_FAVOURITE":
                self.show_gender_list()
            elif postback[0:7] == "FAVOUR_":
                self.favourite = postback[7:].lower()
                self.save()

        elif self.bot_context == "chatting" and postback == "STOP_CHATTING":
            self.unpair()

        elif self.bot_context == "queuing" and postback == "CANCEL_QUEUING":
            self.bot_context = "home"
            self.send_bot_message("Hủy tìm kiếm", "Bạn đã hủy việc tìm kiếm người trò chuyện")
            self.show_menu()
            self.save()
