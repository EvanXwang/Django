# -*- coding: utf-8 -*-
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
from app.models import *
from user.models import *
from app.msg_template import Flex_Msg
from app.linebot_funtion import funtions
from os import path
from datetime import datetime
from linebot.models import (MessageEvent, FollowEvent, PostbackEvent,TextMessage,PostbackAction,TextSendMessage, TemplateSendMessage,ButtonsTemplate,ImageMessage,ImageSendMessage)
from liffpy import (LineFrontendFramework as LIFF,ErrorResponse)
from linebot.models import (ImagemapSendMessage, TextSendMessage, ImageSendMessage, LocationSendMessage, FlexSendMessage, VideoSendMessage,StickerSendMessage, AudioSendMessage)
from linebot.models.template import (ButtonsTemplate, CarouselTemplate, ConfirmTemplate, ImageCarouselTemplate)
from linebot.models.template import *
from linebot.models import PostbackEvent
from linebot.models import (QuickReply,QuickReplyButton,MessageAction)

import re
import requests
import pyimgur
import subprocess
import json






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

    text1 = TextSendMessage(text = 'Hello  ' + name +'!!!'+ '\n感謝您將JoEatJo加入好友！我們會為您分析每餐的營養，並根據個人情況推薦飲食。另外也提供多層面的健康資訊。詳細功能說明請點選圖文選單的「花束」。'+'\n\n請先填寫基本資料 '+'https://liff.line.me/1655708569-ZGkWpwob')
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
    date = datetime.today().date()


    # 呼叫material選單
    if re.search("@", mtext):
        result_message_array = []
        replyJsonPath = "FoodLine/material/" + event.message.text + "/reply.json"
        result_message_array = funtions.detect_json_array_to_new_message_array(replyJsonPath)
        line_bot_api.reply_message(event.reply_token, result_message_array)

    # User個人資料
    elif re.search("#查詢個人資訊", mtext):
        datas = User_type.objects.filter(uid=uid)
        if not datas:  # 判斷是否已填寫基本資訊
            text = TextSendMessage(text='請先填寫個人資訊')
            text1 = TextSendMessage(text='https://liff.line.me/1655708569-ZGkWpwob')
            line_bot_api.reply_message(event.reply_token, [text,text1])
        else:
            message.append(Flex_Msg.person_data(uid))
            line_bot_api.reply_message(event.reply_token, message)

    # 暫時手動輸入食物品項
    elif re.search("eat", mtext):
        job = mtext.split('/')
        datas = Food.objects.filter(en_name=job[1])  # 搜尋Food資料庫記錄，存成 datas
        count = job[2]
        content = funtions.eat_food(datas, uid, name, User_eat, count)
        line_bot_api.reply_message(event.reply_token, [content])

    # 查詢個人一日所需營養值
    elif re.search("#每日所需營養素", mtext):
        user = User_eat.objects.filter(uid=uid)  # 查詢 自己的id
        times = user.filter(created_date__date=date)  # 使用自己的id  搜尋時間
        content = funtions.person_nutrition_fun(times, uid, date)
        line_bot_api.reply_message(event.reply_token, content)

    # 推薦系統
    elif re.search("#隨機推薦", mtext):

        b1, b2, l1, l2, l3, l4, d1, d2, d3, d4 = funtions.recommand_fun()
        message.append(Flex_Msg.recommender_system(b1, b2, l1, l2, l3, l4, d1, d2, d3, d4))
        line_bot_api.reply_message(event.reply_token, message)
    elif re.search("#個人化推薦", mtext):

        text1 = TextSendMessage(text='功能尚未建置完成，請耐心等候')

        line_bot_api.reply_message(event.reply_token, [text1])

    # 自動將https網址轉成 liff
    elif re.search("https://", mtext):
        try:
            # 新增LIFF頁面到LINEBOT中
            liff_id = liff_api.add(view_type="tall", view_url=mtext)
            message.append(TextSendMessage(text='https://liff.line.me/' + liff_id))
            line_bot_api.reply_message(event.reply_token, message)
        except:
            print(err.message)
        return message

    elif re.search("#關於個人資料...", mtext):
        message.append(TextSendMessage(text = '點選圖文選單的「拍立得照片」，即可查詢或更改個人資訊、查詢每日所需營養、查詢當月總表'))
        line_bot_api.reply_message(event.reply_token, message)
    elif re.search("#如何記錄...", mtext):
        message.append(TextSendMessage(text = '點選圖文選單的「拍立得」，只要上傳食物照片，我們會分析食物內容，您可以針對分析出的食物選擇是否添加到紀錄中。'))
        line_bot_api.reply_message(event.reply_token, message)
    elif re.search("#請推薦...", mtext):
        message.append(TextSendMessage(text='點選下方圖文選單的「餐盤」，就能查閱個人化推薦。'))
        line_bot_api.reply_message(event.reply_token, message)

    elif re.search("#我想了解...", mtext):
        message.append(TextSendMessage(text = '請輸入您想查詢的關鍵字'))
        line_bot_api.reply_message(event.reply_token, message)

    elif re.search("#Yes", mtext):

        text1 = TextSendMessage(text='JoEatJo已幫您記錄食物....')
        text2 = StickerSendMessage(package_id=11537, sticker_id=52002735)
        line_bot_api.reply_message(event.reply_token, [text1, text2])

        f = open("resultX.txt", "r")   # 讀取已分析食物名稱
        resultvx = f.read()
        jobs = resultvx.split('/')

        for job in jobs :
            data = Food.objects.filter(en_name=job)  # 搜尋Food資料庫記錄，存成 data (filter會存成list型態)
            tc_food_name = data[0].tc_name
            en_food_name = data[0].en_name
            cal = data[0].cal
            carb = data[0].carb
            pr = data[0].pr
            fat = data[0].fat
            User_eat.objects.create(uid=uid, name=name, tc_name=tc_food_name, en_name=en_food_name,
                                    cal=cal, pr=pr, fat=fat, carb=carb)  # 新增資料於 User_eat資料庫

    elif re.search("#No", mtext):

        text1 = TextSendMessage(text='已取消動作....')
        text2 = StickerSendMessage(package_id=11537, sticker_id=52002753)
        line_bot_api.reply_message(event.reply_token, [text1, text2])

    elif re.search("#手動新增", mtext):

        text1 = TextSendMessage(text='請輸入 eat/食物英文名稱/食物數量')
        line_bot_api.reply_message(event.reply_token, [text1])


    elif re.search('眼睛', mtext):   # 聊天機器人模組 尚未匯入, 此為demo用

        text1 = TextSendMessage(text='狂吐、眼睛痛到睜不開…竟是隱形眼鏡傷角膜！2招避開不良品防眼睛損傷,'+'https://www.edh.tw//article/24902')
        text2 = TextSendMessage(text='眼睛痛大多竟因肩頸僵硬！簡單3動作舒緩眼睛痛,'+'https://www.edh.tw//article/26129')
        text3 = TextSendMessage(text='紅眼≠結膜炎！眼睛痛可能是長皮蛇，這眼周異狀拖久會失明,' + 'https://www.edh.tw//article/24181' )
        text4 = TextSendMessage(text='以下是我為您找到的相關資訊：')

        line_bot_api.reply_message(event.reply_token, [text4, text1, text2, text3])

    # elif re.search(mtext, mtext):   # 聊天機器人模組 尚未匯入
    #     message.append(TextSendMessage(text = '功能還在建構中  .....'))
    #     line_bot_api.reply_message(event.reply_token, message)


    # 測試語法
    elif re.search("測試", mtext):
        foods = Food.objects.all()
        tcname, enname = [], []
        tcname = [food.tc_name  for food in foods]
        for f in tcname:
            print (f)

        message.append(TextSendMessage(text = 'hello'))
        line_bot_api.reply_message(event.reply_token, message)

# ============ QuickReplay =================
@handler.add(PostbackEvent)
def handel_postback_event(event):
    quick_reply_list = funtions.postback_fun(event)
    line_bot_api.reply_message(event.reply_token,TextSendMessage('已新增記錄，謝謝你的喜歡'))

from PIL import Image
# ============ 食物辨識model =================
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    file_name = './scan.jpg'




    weight_name = './custom-yolov4-detector_best0213.weights'
    with open(file_name, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    img = Image.open("./scan.jpg")
    img.thumbnail((512, 512))
    img.save("./scan1.jpg")
    file_name = './scan1.jpg'
    some_command = """./darknet detect cfg/custom-yolov4-detector.cfg %s %s -ext_output -dont-show > result.txt""" % (
        weight_name, file_name)

    p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()

    # This makes the wait possible
    p_status = p.wait()

    # print("Command output: " + output)

    f = open("result.txt", "r")
    lines = f.readlines()

    datas = []

    for x in range(len(lines)):
        if "left_x" not in lines[x]:
            continue
        else:
            datas.append(lines[x])

    w, h = 5, len(datas)
    Matrix = [[0 for x in range(w)] for y in range(h)]

    bans = ["t", "w", "h", ")"]

    for x in range(len(datas)):
        c = 0
        while datas[x][c] != ":":
            c += 1
        Matrix[x][0] = datas[x][0:c]
        for y in range(1, 5):
            c += 1
            while datas[x][c] != ":":
                c += 1
            c += 1
            cx = c
            while datas[x][c] not in bans:
                c += 1
            Matrix[x][y] = int(datas[x][cx:c])

    string = ""

    for x in range(len(datas)):
        for y in range(0, 1):
            string += str(Matrix[x][y])
            #string += " "
        if x != len(datas)-1:
            string += '/'

    f = open("resultX.txt", "w")
    f.write(string)
    f.close()

    # open and read the file after the appending:
    f = open("resultX.txt", "r")
    # print(f.read())

    resultvx = f.read()

    if len(datas) == 0:
        if path.exists(weight_name):
            resultvx = "資料庫無建檔!!!"  # No results are found!!!
        else:
            resultvx = "Weights not found!!!"

    # Note Name, left, top, width, height

    CLIENT_ID = "650aefc02187ffd"
    PATH = "./predictions.jpg"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    images = uploaded_image.link

    uid = event.source.user_id
    profile = line_bot_api.get_profile(uid)
    name = profile.display_name
    jobs = resultvx.split('/')
    message = []

    if resultvx == '資料庫無建檔!!!':

        qrb2 = QuickReplyButton(action=MessageAction(label='取消', text='#No'))
        qrb1 = QuickReplyButton(action=MessageAction(label='手動新增', text='#手動新增'))
        quick_reply_list = QuickReply([qrb1, qrb2])

        text1 = TextSendMessage(text='資料庫無建檔!!!')
        text2 = TextSendMessage('是否手動新增食物： ' , quick_reply=quick_reply_list)
        line_bot_api.reply_message(event.reply_token, [text1, text2])

    else : # 辨識成功

        # QuickReply 選項
        qrb1 = QuickReplyButton(action=MessageAction(label='資料正確', text='#Yes' ))
        qrb2 = QuickReplyButton(action=MessageAction(label='取消', text='#No'))
        qrb3 = QuickReplyButton(action=MessageAction(label='手動新增', text='#手動新增'))
        quick_reply_list = QuickReply([qrb1, qrb2, qrb3])

        # 搜尋Food資料庫記錄，存成 data (filter會存成list型態)
        tcname = []
        for job in jobs:
            data = Food.objects.filter(en_name=job)
            tcname.append(data[0].tc_name)

        # 計算食物數量
        eat_list = dict((a, str(tcname.count(a)) + '份') for a in tcname);

        # 將字典key & values 值取出  (因為要去除{""})
        foods_list = []
        for key, values in eat_list.items():
            foods_list.append(key + values)

        # 去除list的['']
        food = ''.join(foods_list)

        text1 = TextSendMessage(text ='辨識食物如下：')
        text2 = ImageSendMessage(original_content_url=images, preview_image_url=images)
        text3 = TextSendMessage('是否新增食物： '+ str(food) ,quick_reply=quick_reply_list)

        line_bot_api.reply_message(event.reply_token, [text1, text2, text3])

