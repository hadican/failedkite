import logging

from flask import Flask, request

from config import Config
from notification_service import NotificationService
from slack_client import SlackClient

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

config = Config()
slack_client = SlackClient(token=config.slack_token)
notification_service = NotificationService(slack_client, config)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    build = data.get("build", {})
    if not build:
        return "Invalid build information received.", 400

    message, status_code = notification_service.notify(build)
    return message, status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
