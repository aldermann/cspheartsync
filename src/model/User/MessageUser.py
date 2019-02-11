from model.User.DBUser import DBUser


class MessageUser(DBUser):
    def send_text_message(self, message):
        self._API.send_text_message(self.messenger_id, message)

    def send_attachment(self, content_type, content):
        self._API.send_attachment(self.messenger_id, content_type, content)
