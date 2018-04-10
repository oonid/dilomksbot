# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ElementTree
from datetime import datetime

from flask import Blueprint, request
from logging import info, error

from google.appengine.api import urlfetch  # replace with urllib2 or requests for development

from telegram import broadcast_to_telegram_groups
from datastore import DiloEvent


__author__ = 'oon arfiandwi'


scheduler = Blueprint('scheduler', __name__, template_folder='templates', static_folder='asset')


def get_dilo_makassar_event(index):
    event = None
    urlfetch.set_default_fetch_deadline(55)
    result = urlfetch.fetch(url='http://makassar.dilo.id/event-mkssr?start={}&format=feed&type=rss'.format(index),
                            method=urlfetch.GET)
    info(str(result.status_code))
    # print result.headers
    if result.status_code != 200:
        error(result.content)
    else:
        content = result.content
        info(content)
        feed = ElementTree.fromstring(content)
        channel = feed.find("channel")
        items = channel.findall("item")
        for item in items:
            title = item.find('title')
            link = item.find('link')
            description = item.find('description')
            event = {
                'title': title.text,
                'link': link.text,
                'description': description.text,
            }

    return event


def get_event_message(title, link):
    emoji_hello = u'\U0001F44B'
    emoji_airplane = u'\U00002708' + u'\U0000FE0F'
    return u'''\nHalo DILovers! {}
DILo Makassar ada event baru nih, ikutan yuk..\n
Event kali ini tentang <strong>{}</strong>\n
{} <a href="{}">Kunjungi situs DILo untuk info lebih lanjut</a>\n'''.format(emoji_hello, title, emoji_airplane, link)


@scheduler.route('/scheduler/visit-dilo-makassar', methods=['GET'])
def visit_dilo_makassar():

    if request.method == 'GET':
        for idx in range(0, 10):  # check last 10 events
            event = get_dilo_makassar_event(idx)
            if event:  # found event, not None
                info(event['title'])
                info(event['link'])
                info(event['description'])
                # using Google Datastore as Database
                diloevent = DiloEvent.get_by_id(event['link'])  # link is unique, so we use it as id
                if diloevent is None:

                    # save to datastore only if "new" event
                    diloevent = DiloEvent(id=event['link'],
                                          title=event['title'],
                                          link=event['link'],
                                          description=event['description'],
                                          sendnotification=False,
                                          updated=datetime.utcnow())
                    diloevent.put()

                if not diloevent.sendnotification:
                    # send notification only if "new" event (not sendnotification yet)
                    broadcast_to_telegram_groups(get_event_message(diloevent.title, diloevent.link))
                    diloevent.sendnotification = True  # update datastore after send notification
                    diloevent.put()

    return ''
