import zulip
import json
import requests

import re
from credentials import bot_key, bot_email

client = zulip.Client(email=bot_email,
                      api_key=bot_key)

# call respond function when client interacts with kudos bot
def respond(msg):
    print msg

    if (msg['sender_email'] != "kudos-bot@students.hackerschool.com"
        and msg['type'] == 'private'):
            
        if re.search(r'@\*\*.+\*\*', msg['content']):

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