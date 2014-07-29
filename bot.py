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

#Note to self: example msg in credentials.