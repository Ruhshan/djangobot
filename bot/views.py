from django.shortcuts import render
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.conf import settings

PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN
VERIFY_TOKEN = settings.VERIFY_TOKEN

from .interactions import *

class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                pprint(message)
                if 'message' in message:
                    sender_id = message["sender"]["id"]
                    recipient_id = message["recipient"]["id"]
                    pprint(message)

                    message_type=get_message_type(message)

                    if message_type == 'quick_reply':
                        payload, id = message['message']['quick_reply']['payload'].split('.')
                        if payload == "cat":
                            #send_message(sender_id, 'Thanks for quick reply {}# {}'.format(payload, id))
                            send_menu(sender_id, id)
                        else:
                            send_message(sender_id, "un recognized category")

                    elif message_type == 'simple_message':

                        message_text = message["message"]["text"]
                        pprint(message_text)

                        if message_text == 'start':
                            start_conversation(sender_id)
                        elif PendingOrder.objects.filter(customer_id=sender_id, is_delivered=False, is_confirmed=False, recipt_provided=False).exists():
                            take_info(sender_id, message_text)
                        else:
                            send_message(sender_id, "Sorry!")
                    else:
                        send_message(sender_id, "Unable to understand message type")
                if "postback" in message:
                    sender_id = message["sender"]["id"]
                    recipient_id = message["recipient"]["id"]
                    payload, id = message['postback']['payload'].split('.')
                    pprint(message)
                    if payload=="item":
                        take_order(sender_id, id)
                    else:
                        pass

                    #send_message(sender_id, "{}#{}".format(payload, id))

        return HttpResponse()