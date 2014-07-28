import requests
import json
from collections import namedtuple

from credentials import bot_key, bot_email

Message = namedtuple('Message', 'text, sender')

class Bot(object):
    """ A bot to send you emojis. """
    def __init__(self):
        self.bot_name = "@**Kudos Bot**"
        base_url = "https://zulip.com/api/v1/"
        self.register_url = base_url + "register"
        self.events_url = base_url + "events"
        self.message_url = base_url + "messages"

        humbug_key = bot_key
        humbug_user = bot_email
        self.bot_auth = (humbug_user, humbug_key)
        self.last_event_id = -1

        self.register_for_messages()

    def start(self):
        while True:
            response = self.listen_on_queue()
            self.parse_and_dispatch(response)

    def register_for_messages(self):
        params = {"event_types" : ['messages']}
        r = requests.post(self.register_url, auth=self.bot_auth, params=json.dumps(params))
        self.q_id = r.json()['queue_id']

    def listen_on_queue(self):
        params = {"queue_id": self.q_id, "last_event_id": self.last_event_id}
        r = requests.get(self.events_url, auth=self.bot_auth, params=params)
        return r.json()

    def parse_and_dispatch(self, response):
        for event in response['events']:
            if event.has_key('message'):
                sender = event['message']['sender_email']
                b.last_event_id = event['message']['id']
                if sender != "emoji-bot@students.hackerschool.com":
                    msg = Message(event['message']['content'], event['message']['sender_email'])
                    self.dispatch_on(msg)

    def dispatch_on(self, message):
        print message
        self.reply(message.sender, message.text)

    def reply(self, recipient, content):
        params = {"type": "private",
                  "to": recipient,
                  "content": content}
        r = requests.post(self.message_url, auth=self.bot_auth, data=params)
        # print r.content
        # print r.request.url


if __name__ == "__main__":
    b = Bot()
    b.start()
