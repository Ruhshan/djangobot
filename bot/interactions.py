import os
import sys
import json
from datetime import datetime
from pprint import pprint

import requests

from django.conf import settings
PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN
VERIFY_TOKEN = settings.VERIFY_TOKEN
from .models import ItemCategory, PendingOrder

def get_message_type(message):

    if 'quick_reply' in message['message'].keys():
        return 'quick_reply'
    else:
        return 'simple_message'

def get_user_details(recipient_id):
    user_details_url = "https://graph.facebook.com/v2.6/%s" % recipient_id
    user_details_params = {'fields': 'first_name,last_name,profile_pic',
                           'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()

    return user_details


def deliver(recipient_id, message):
    #log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message['text']))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": message
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_category(recipient_id):
    quick_replies = []
    for cat in ItemCategory.objects.all():
        reply = {"content_type" : "text", "title": cat.name, "payload": cat.payload_code}
        quick_replies.append(reply)

    category = {
        "text" : "I Have these options for you today:",
        "quick_replies": quick_replies
        }
    deliver(recipient_id,category)

def send_menu(recipient_id, cat_id):
    items = ItemCategory.objects.get(id=int(cat_id)).item_set.all()
    elements=[]
    for item in items:
        element = {
        "title": item.name,
        "subtitle": "Price: {} Tk".format(item.price),
        "image_url":  item.image,
        "buttons": [
                {
                "type": "postback",
                "title": "Get {}".format(item.name),
                "payload": item.postback_code,
                }
            ],
        }
        elements.append(element)


    attachment = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements

            }
        }
                  }
    deliver(recipient_id, attachment)

def take_order(recipient_id):
    customer = get_user_details(recipient_id)
    order = PendingOrder(customer_id=recipient_id, customer_name=customer['first_name']+customer["last_name"], address="take_now")
    order.save()
    send_message(recipient_id, "Please provide your address")

def start_conversation(recipient_id):
    user_info = get_user_details(recipient_id)
    send_message(recipient_id, "Hi %s, It's wonderful to see you today!" % user_info['first_name'])
    send_category(recipient_id)


def send_message(recipient_id, message_text):
    deliver(recipient_id,{"text": message_text})


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = msg
        print("{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()

