from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from linebot.models import (MessageEvent, FollowEvent, PostbackEvent,TextMessage,PostbackAction,TextSendMessage, TemplateSendMessage,ButtonsTemplate,ImageMessage,ImageSendMessage)
from liffpy import (LineFrontendFramework as LIFF,ErrorResponse)
from linebot.models import (ImagemapSendMessage, TextSendMessage, ImageSendMessage, LocationSendMessage, FlexSendMessage, VideoSendMessage,StickerSendMessage, AudioSendMessage)

from linebot.models.template import *


import re

# Create your views here.

# ============ 需到FoodLine/settings.py 新增 line相關key =================
liff_api = LIFF(settings.LINE_CHANNEL_ACCESS_TOKEN)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)



# ============ 用戶關注 =================
@handler.add(FollowEvent)
def handle_follow(event):
    uid = event.source.user_id
    profile = line_bot_api.get_profile(uid)
    name = profile.display_name
    pic_url = profile.picture_url

    if User_Info.objects.filter(uid=uid).exists() == False:

        User_Info.objects.create(uid=uid, name=name, pic_url=pic_url)

    text1 = TextSendMessage(text = 'Hello  ' + name +'!!!')
    text2 = StickerSendMessage(package_id=11537, sticker_id=52002768)
    line_bot_api.reply_message(event.reply_token,[ text1, text2])
@csrf_exempt
def callback(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        global domain
        domain = request.META['HTTP_HOST']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# ============ 用戶訊息 =================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    message = []
    uid = event.source.user_id
    profile = line_bot_api.get_profile(uid)
    name = profile.display_name


    if re.search(mtext, mtext):   # 聊天機器人模組 尚未匯入
        message.append(TextSendMessage(text = mtext+"!!!"))
        line_bot_api.reply_message(event.reply_token, message)