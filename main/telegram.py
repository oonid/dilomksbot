# -*- coding: utf-8 -*-

from flask import Blueprint, request
from decouple import config
from json import dumps
from datetime import datetime
from logging import info

from google.appengine.api import urlfetch  # replace with urllib2 or requests for development

from main.datastore import TelegramGroup


__author__ = 'oon arfiandwi'

# load variables from hidden environment or from environment variable
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
TELEGRAM_DILOMKSBOT_ID = config('TELEGRAM_DILOMKSBOT_ID', cast=long)


telegram = Blueprint('telegram', __name__, template_folder='templates', static_folder='asset')


def add_chat_to_broadcast_list(chat):
    try:
        g = TelegramGroup.get_by_id(str(chat['id']))
        if g is None:
            g = TelegramGroup(id=str(chat['id']),
                              tgid=chat['id'],
                              info=chat['title'],
                              updated=datetime.utcnow())
            g.put()
    except TelegramGroup.DoesNotExists:
        g = TelegramGroup(id=str(chat['id']),
                          tgid=chat['id'],
                          info=chat['title'],
                          updated=datetime.utcnow())
        g.put()


@telegram.route('/webhook/'+TELEGRAM_TOKEN, methods=['POST'])
def webhook():

    if request.method == 'POST':
        if request.json is not None:
            bot_added_to_group = False
            j = request.json
            info(j)  # currently we won't response any chat, only log chat
            if 'message' in j:
                if 'new_chat_members' in j['message']:
                    for member in j['message']['new_chat_members']:
                        # if bot added to group, get 'new_chat_members' message (included the bot it self)
                        if member['is_bot'] and member['id'] == TELEGRAM_DILOMKSBOT_ID:
                            bot_added_to_group = True

                # process if bot added to group
                if bot_added_to_group:
                    if 'chat' in j['message']:
                        chat = j['message']['chat']
                        if 'type' in chat and (chat['type'] == 'group' or chat['type'] == 'supergroup'):
                            add_chat_to_broadcast_list(chat)

    return ''


def broadcast_to_telegram_groups(new_data_message):

    for tg in TelegramGroup.query():  # retrieve all telegram groups
        msg_data = {
            'chat_id': tg.tgid,
            'text': new_data_message[:4000] if len(new_data_message) > 4000 else new_data_message,  # max 4096
            'parse_mode': 'HTML'
        }
        urlfetch.set_default_fetch_deadline(55)
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:32.0) Gecko/20100101 Firefox/32.0",
            "Connection": "keep-alive",
        }
        result = urlfetch.fetch(url='https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN),
                                payload=dumps(msg_data),
                                method=urlfetch.POST,
                                headers=headers)
        info(result.status_code)
        info(result.content)

        # remove group if not accessible
        if result.status_code == 403:
            # {"ok":false,"error_code":403,"description":"Forbidden: bot was kicked from the supergroup chat"}
            # {"ok":false,"error_code":403,"description":"Forbidden: bot is not a member of the supergroup chat"}
            info('remove TelegramGroup {} ({})'.format(tg.tgid, tg.info))
            tg.key.delete()
