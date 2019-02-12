from abc import ABC, abstractmethod


class APIInterface(ABC):

    @abstractmethod
    def get_url(self, api_path):
        raise NotImplementedError

    @abstractmethod
    def get_user_data(self, messenger_id):
        raise NotImplementedError

    @abstractmethod
    def send(self, recipient_id, payload):
        raise NotImplementedError

    @abstractmethod
    def send_text_message(self, recipient, message, quick_replies):
        raise NotImplementedError

    @abstractmethod
    def send_attachment(self, recipient, content_type, content):
        raise NotImplementedError

    @abstractmethod
    def send_generic_template(self, recipient, elements):
        raise NotImplementedError
