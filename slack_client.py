import logging

from slack import WebClient


class SlackClient:
    def __init__(self, token):
        self.client = WebClient(token=token)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_user_id_by_email(self, email):
        try:
            response = self.client.users_lookupByEmail(email=email)
            if response["ok"]:
                return response["user"]["id"]
            else:
                self.logger.error("Failed to fetch user ID for email=%s error=%s", email, response["error"])
                return None
        except Exception as e:
            self.logger.error("Error fetching user ID for email=%s error=%s", email, str(e))
            return None

    def send_message(self, message, user_id):
        try:
            response = self.client.chat_postMessage(channel=user_id, text=message)
            if response["ok"]:
                return True
            else:
                self.logger.error("Failed to send Slack message with error=%s", response["error"])
                return False
        except Exception as e:
            self.logger.error("Failed to send Slack message with error=%s", str(e))
            return False
