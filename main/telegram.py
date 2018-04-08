# -*- coding: utf-8 -*-

from flask import Blueprint, request
from decouple import config
from json import dumps
from logging import info

from google.appengine.api import urlfetch  # replace with urllib2 or requests for development

__author__ = 'oon arfiandwi'

# load variables from hidden environment or from environment variable
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
TELEGRAM_GROUP_DILO_MKS_ID = config('TELEGRAM_GROUP_DILO_MKS_ID', cast=long)


telegram = Blueprint('telegram', __name__, template_folder='templates', static_folder='asset')


@telegram.route('/webhook/'+TELEGRAM_TOKEN, methods=['POST'])
def webhook():

    if request.method == 'POST':
        if request.json is not None:
            info(request.json)  # currently we won't response any chat

    return ''


def send_message_to_dilo_mks_group(new_data_message):
    msg_data = {
        'chat_id': TELEGRAM_GROUP_DILO_MKS_ID,
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
