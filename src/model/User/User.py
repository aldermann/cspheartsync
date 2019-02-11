from model.User.MessageUser import MessageUser


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
            self.send_text_message("Is queuing now")
        else:
            self.partner = partner_id
            self.bot_context = "chatting"
            self.send_text_message("You are paired now")
            self.save()
            partner = User(partner_id)
            partner.partner = self.messenger_id
            partner.bot_context = "chatting"
            self.send_text_message("You are paired now")
            partner.save()

    def unpair(self):
        partner = User(self.partner)
        partner.partner = None
        partner.bot_context = "home"
        self.send_text_message("You've been disconnected")
        partner.save()
        self.partner = None
        self.bot_context = "home"
        self.send_text_message("You've disconnected")
        self.save()

    def forward_message(self, message):
        partner = User(self.partner)
        partner.send_text_message(message)

    def process_message(self, message):
        if self.bot_context == "home":
            self.pair()
        elif self.bot_context == "chatting":
            if message != "end_chat":
                self.unpair()
            else:
                self.forward_message(message)
        elif self.bot_context == "queuing":
            self.send_text_message("please wait")
