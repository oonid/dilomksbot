# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ElementTree

from flask import Blueprint, request
from logging import info, error

from google.appengine.api import urlfetch  # replace with urllib2 or requests for development

from telegram import send_message_to_dilo_mks_group

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
        event = get_dilo_makassar_event(0)
        if event:  # found event, not None
            info(event['title'])
            info(event['link'])
            info(event['description'])
            send_message_to_dilo_mks_group(get_event_message(event['title'], event['link']))

    return ''
