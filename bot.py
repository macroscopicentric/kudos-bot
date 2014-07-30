import zulip
import re
import logging

from credentials import bot_key, bot_email

#Logger is to maintain a record of messages sent to kudos-bot. However, requests (used by zulip) logs HTTPS connection requests at the info level. Filter is to avoid actually logging these.
class SkipHTTPConnectionsFilter(logging.Filter):
    def filter(self, record):
        if 'Starting new HTTPS connection' not in record.getMessage():
            return record.getMessage()

# call respond function when client interacts with kudos bot
def respond(msg):

    if (msg['sender_email'] != "kudos-bot@students.hackerschool.com"
        and msg['type'] == 'private'):
            
        if re.search(r'@\*\*.+\*\*', msg['content']):

            logger.info(msg)
            client.send_message({
                "type": "stream",
                "subject": "kudos-test",
                "to": "test-bot",
                "content": "%s" % msg['content']
            })

        else:
            client.send_message({
                "type": msg['type'],
                "subject": msg['subject'],
                "to": msg['sender_email'],
                "content": '''I'm sorry, I only forward messages that @-mention the person you want to give kudos too.'''
            })

if __name__ == '__main__':
    client = zulip.Client(email=bot_email, api_key=bot_key)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(filename="bot.log")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    # logging.basicConfig(filename='bot.log', format='%(asctime)s %(message)s', level=logging.INFO)
    # This is a blocking call that will run forever
    client.call_on_each_message(lambda msg: respond(msg))

"""
Example msg:

{
    "recipient_id": XXXXX,
    "sender_email": "email@email.com",
    "timestamp": XXXXXXXXXX,
    "display_recipient": [
        {
            "domain": "students.hackerschool.com",
            "short_name": "kudos-bot",
            "email": "kudos-bot@students.hackerschool.com",
            "full_name": "Kudos Bot",
            "id": XXXX
        },
        {
            "full_name": "Full Name",
            "domain": "students.hackerschool.com",
            "email": "email_username@email.com",
            "short_name": "email_username",
            "id": XXXX
        }
    ],
    "sender_id": XXXX,
    "sender_full_name": "Full Name",
    "sender_domain": "students.hackerschool.com",
    "content": "message",
    "gravatar_hash": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "avatar_url": "https://url.com",
    "client": "website",
    "content_type": "text/x-markdown",
    "subject_links": [],
    "sender_short_name": "email_username",
    "type": "private" or "stream",
    "id": XXXXXXXX,
    "subject": "topic",
    ("to": "stream")
}

("to" isn't included if it's a private message.)
"""