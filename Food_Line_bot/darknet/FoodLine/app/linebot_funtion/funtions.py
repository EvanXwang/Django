# -*- coding: utf-8 -*-
from linebot.models import *
from app.msg_template import Flex_Msg
from user.models import *
import json
import datetime
import chardet
import numpy as np
import pandas as pd
import re

# 暫時手動輸入食物品項
def eat_food(datas,uid,name,User_eat, count):
    message = []

    for i in range (int(count)):
        for data in datas:  # 依序把資料存成字串
            tc_food_name = data.tc_name
            en_food_name = data.en_name
            cal = data.cal
            carb = data.carb
            pr = data.pr
            fat = data.fat
            User_eat.objects.create(uid=uid, name=name, tc_name=tc_food_name, en_name=en_food_name,
                                    cal=cal, pr=pr, fat=fat, carb=carb)  # 新增資料於 User_eat資料庫

            message = (TextSendMessage (text= '已記錄：'+tc_food_name+count+'份'+'\n\n' +'每份營養值如下：'+'\n' 
                                                '熱量' + str(cal)+' Cal' +'\n'+
                                                '蛋白質' + str(pr)+' g' +'\n'+
                                                '脂肪' + str(fat)+' g' +'\n'+
                                                '醣類' + str(carb)+' g'))

    return message


# 查詢個人一日所需營養值
def person_nutrition_fun(times, uid, date ):

    message = []
    cal, pr, fat, carb = 0, 0, 0, 0
    for time in times:  # 依序把資料存成字串
        cal = cal + time.cal
        pr = pr + time.pr
        fat = fat + time.fat
        carb = carb + time.carb

    user = User_eat.objects.filter(uid=uid)  # 查詢 自己的id
    user_eat_list = user.filter(created_date__date=date)

    food_list = []
    for list in user_eat_list:
        food_list.append(list.tc_name)

    eat_list = dict((a, str(food_list.count(a)) + '份') for a in food_list);

    if eat_list == {}:
        food = '今天還沒有飲食記錄喔....'
    else:
        foods_list = []
        for key,values in eat_list.items():
            foods_list.append(key + values)

        food = '、'.join(foods_list)


   

    message.append(TextSendMessage(text='每日所需各種營養素如下，請均衝飲食喔：'))
    message.append(Flex_Msg.person_nutrition(uid))
    message.append(TextSendMessage(text=str(food)))
    message.append(TextSendMessage(text=str(date) + ' 營養總計如下：'))
    message.append(TextSendMessage(text="熱量" + str(round(cal, 2))+' Cal'+
                                        '  脂質' + str(round(fat, 2))+' g'+
                                        '  醣類' + str(round(carb, 2))+' g'+
                                        '  蛋白質' + str(round(pr, 2))+' g'))
    return message


# ============ 推薦系統 =================
def recommand_fun():

    food = pd.DataFrame(list(Food.objects.all().values()))

    # food["FAT"] = food["FAT"].map(lambda x: np.nan if x == "Unknown" else x)  # 將Unknown即沒有填的資料換成平均值
    # food["FAT"].fillna(food["FAT"].median(), inplace=True)
    # food["CARB"] = food["CARB"].map(lambda x: np.nan if x == "Unknown" else x)  # 將Unknown即沒有填的資料換成平均值
    # food["CARB"].fillna(food["CARB"].median(), inplace=True)

    # rating特徵轉浮點數，空值補平均值 #原本註解
    # #.astype:對資料型別進行轉換
    food["cal"] = food["cal"].astype(float)  # 特徵轉浮點數，這裡純數字 沒空值
    food["pr"] = food["pr"].astype(float)  # 特徵轉浮點數，這裡純數字 沒空值

    food1x = []  # 主食 配菜 甜點 飲料 湯 水果
    food1y = []
    food2x = []
    food3x = []
    food4x = []
    food5x = []
    food6x = []

    for x in range(len(food)):
        if food.loc[x]["cat"] == "主食" and food.loc[x]["meal"] == "breakfast":
            food1x.append(x)
        elif food.loc[x]["cat"] == "主食" and food.loc[x]["meal"] == "lunch, dinner":
            food1y.append(x)
        elif food.loc[x]["cat"] == "配菜":
            food2x.append(x)
        elif food.loc[x]["cat"] == "甜點":
            food3x.append(x)
        elif food.loc[x]["cat"] == "飲料":
            food4x.append(x)
        elif food.loc[x]["cat"] == "湯":
            food5x.append(x)
        elif food.loc[x]["cat"] == "水果":
            food6x.append(x)

    # 將genre特徵轉換成onehot encoder  #原本註解
    # One Hot encoding的編碼邏輯為將類別拆成多個行(column)，
    # 每個列中的數值由1、0替代，當某一列的資料存在的該行的類別則顯示1，反則顯示0。
    # pd.concat 資料合併 axis=1:行合併
    # [anime["genre"].str.get_dummies(sep=",") : 回傳genre的內容用,分割後的字串 然後如果有這個ndex就標1 沒有標0
    # pd.get_dummies(anime[["type"]]) :回傳type的內容，然後如果有這個ndex就標1 沒有標0
    # anime[["rating"]] 合併
    # anime[["members"]]合併
    # anime["episodes"]] 合併
    food_features = pd.concat([food["meal"].str.get_dummies(sep=","),  # meal欄位 用逗號  #這裡中括號多寡注意
                               pd.get_dummies(food["cat"]),
                               food["cal"], food["pr"],
                               food["fat"], food["carb"]], axis=1)
    # 正則表達式參考網址
    # https://blog.csdn.net/Yellow_python/article/details/80543937
    # https://ithelp.ithome.com.tw/articles/10209446
    # \W: 任何非數字字母底線，相當於 [^A-Za-z0-9_]
    # re.sub(pattern, repl, string, count=0, flags=0)
    # pattern : 匹配的正則表達式(字串)
    # repl : 替换的字符串，也可为一個函数。
    # string : 要被查找替换的原始字符串。
    # count : 模式匹配後替换的最大次数，默認0表示替换所有的匹配。
    # flags=re.I (忽略大小寫)  re.M(可以輸出多個) re.S(會有\n等符號加字)
    # 下面這行是把name取代成 re.sub('\W+'," ", name) (把非數字字母底線換成空白)
    food["en_name"] = food["en_name"].map(lambda name: re.sub('\W+', " ", name))  # 這行要研究  這裡只有改欄位名字
    # print(food_features.head())  # 特徵表格  進系統可以註解

    # 使用MinMaxScaler 幫助標準化 加速運算速度#原本註解
    # MinMaxScaler(最小最大值標準化) 把資料放到[0,1]之間
    from sklearn.preprocessing import MinMaxScaler
    min_max_scaler = MinMaxScaler()
    food_features = min_max_scaler.fit_transform(food_features)  # fit_transform先訓練再轉換
    np.round(food_features, decimals=2)  # 四捨五入，到小數點第2位

    # print(anime_features)

    # 引入最近鄰 #原本註解
    from sklearn.neighbors import NearestNeighbors
    # n_neighbors選幾個鄰居，algorithm有 'brute'、'kd_tree' 和 'ball_tree'
    # fit(從什麼==(anime_features)學習模型參數)
    nbrs = NearestNeighbors(n_neighbors=4, algorithm='ball_tree').fit(food_features)  # 這裡可變
    distances, indices = nbrs.kneighbors(food_features)

    # indices 為一個[],第一個element 是動畫自己的ID，後面的element是最相似(推薦的)的動畫ID #原本註解
    # 返回值indices：第0列元素为参考点的索引，后面是(n_neighbors - 1)个与之最近的点的索引
    # 返回值distances：第0列元素为与自身的距离(为0)，后面是(n_neighbors - 1)个与之最近的点与参考点的距离

    # 設立function幫助查找  #原本註解
    def get_index_from_name(name):
        # 在dataframe中根據一定的條件，得到符合條件的某行
        return food[food["en_name"] == name].index.tolist()[0]  # 回傳條件符合的行號

    # 把csv中EN_NAME列的值全部變一個list
    all_food_names = list(food.en_name.values)

    def get_id_from_partial_name(partial):  # 查關鍵字，例如查一拳超人 會有一拳超人1,2,3等
        for name in all_food_names:
            if partial in name:
                print(name, all_food_names.index(name))  # 輸出名稱跟行號

    # get_id_from_partial_name("Naruto")

    def print_similar_food(query=None, id=None):
        if id:  # 用id查
            output = []
            for id in indices[id][1:]:  # [編號一到全部]
                # output.append(food.loc[id]["EN_NAME"])#設一個空list存入英文名字跟中文名字
                output.append(food.loc[id]["tc_name"])
            return output  # .loc:用具體標籤查詢 用EN_NAME,TC_NAME列查  英文名字跟中文名字
        if query:  # 用名稱查
            found_id = get_index_from_name(query)  # 查到名稱所在的行號
            output = []
            for id in indices[found_id][1:]:  # [編號一到全部]
                # output.append(food.loc[found_id]["EN_NAME"]) #設一個空list存入英文名字跟中文名字
                output.append(food.loc[found_id]["tc_name"])
            return output  # .loc:用具體標籤查詢 用EN_NAME,TC_NAME列查  英文名字跟中文名字

    # 用query查
    # print_similar_food(query="cold noodles") #跟XX像的食物
    # print_similar_animes("Mushishi")
    # print_similar_animes("Fairy Tail")
    # 用id查
    # print_similar_animes(id=719) #第幾行 跟第719行的食物最接近的3個食物

    # 輸出範例
    # 早餐：主食＋飲料	[肉包 , 玄米茶]
    # 午餐：主食＋配菜＋湯＋甜點	[肉醬義大利麵 , 水煮蛋 , 番茄蛋湯 , 奇異果乾 ]
    # 晚餐：主食＋配菜＋湯＋水果	[蚵仔煎 , 鮪魚花椰菜沙拉 , 餛飩湯 , 葡萄柚 ]

    import random  # 冷啟動 用隨機處理
    def coldstart(mode):
        def test(ser=None):
            # a = ser  #輸入的食物
            # found_id = get_index_from_name(a)  # 查到名稱所在的行號
            found_id = ser
            out = print_similar_food(id=ser)
            return out

        # 把主食也做隨機就不再指定水煎包

        ran = int(random.random() * len(food1x))
        val1 = test(ser=food1x[ran])  # 蛋餅 主食又breakfast
        # print(val1)
        ran = int(random.random() * len(food1y))
        val1y = test(ser=food1y[ran])
        ran = int(random.random() * len(food2x))
        val2 = test(ser=food2x[ran])  # 皮蛋 配菜又dinner lunch
        # print(val2)
        ran = int(random.random() * len(food3x))
        val3 = test(ser=food3x[ran])  # 芒果乾 甜點 other
        # print(val3)
        ran = int(random.random() * len(food4x))
        val4 = test(ser=food4x[ran])  # 草莓牛奶 飲料 又breakfast
        # print(val4)
        ran = int(random.random() * len(food5x))
        val5 = test(ser=food5x[ran])  # 海帶 湯 dinner lunch
        # print(val5)
        ran = int(random.random() * len(food6x))
        val6 = test(ser=food6x[ran])  # 櫻桃  水果 other
        # print(val6)

        a = []
        # 早餐：主食＋飲料	[肉包 , 玄米茶]
        # 午餐：主食＋配菜＋湯＋甜點	[肉醬義大利麵 , 水煮蛋 , 番茄蛋湯 , 奇異果乾 ]
        # 晚餐：主食＋配菜＋湯＋水果

        if mode == 1:  # 早餐 主食＋飲料
            i = random.randint(0, 2)

            b1 = val1[i]
            b2 = val4[i]

            return b1, b2

        if mode == 2:  # 午餐：主食＋配菜＋湯＋甜點
            i = random.randint(0, 2)

            l1 = val1[i]
            l2 = val2[i]
            l3 = val5[i]
            l4 = val3[i]
            return l1, l2, l3, l4

        if mode == 3:  # 晚餐：主食＋配菜＋湯＋水果
            i = random.randint(0, 2)

            d1 = val1[i]
            d2 = val2[i]
            d3 = val5[i]
            d4 = val6[i]
            return d1, d2, d3, d4

    b1, b2 = coldstart(mode=1)
    l1, l2, l3, l4 = coldstart(mode=2)
    d1, d2, d3, d4 = coldstart(mode=3)

    return b1, b2, l1, l2, l3, l4, d1, d2, d3, d4


# 判斷 @ 物件
def detect_json_array_to_new_message_array(fileName):
    # 開啟檔案，轉成json
    with open(fileName, encoding='utf8') as f:
        jsonArray = json.load(f)

    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')

        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'video':
            returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))
    return returnArray


# ============ QuickReplay =================
def postback_fun(event):
    postback_data = event.postback.data

        # qrb1 = QuickReplyButton(action=MessageAction(label='資料正確', text='正確'))
        # qrb2 = QuickReplyButton(action=MessageAction(label='想在重拍', text='重拍'))
        # qrb3 = QuickReplyButton(action=LocationAction(label="傳送位置"))
        # qrb4 = QuickReplyButton(action=CameraAction(label="拍照"))
        # qrb5 = QuickReplyButton(action=CameraRollAction(label="相簿"))
        # qrb6 = QuickReplyButton(action=DatetimePickerAction(label="時間選擇",data="時間選擇",mode='datetime'))

    qrb1 = QuickReplyButton(action=MessageAction(label='Yes', text='eat/' + postback_data))  # 寫入資料庫
    qrb2 = QuickReplyButton(action=MessageAction(label='No', text='已取消'))
    quick_reply_list = QuickReply([qrb1, qrb2])

    if postback_data == 'apple':
        return quick_reply_list

    elif postback_data == 'tianbula':
        return quick_reply_list

    elif postback_data == 'like':
        return quick_reply_list


# def ai_talk():
# elif (event.message.text.find('@') != 1):
#     myuid = "Line"
#     mymsg = event.message.text
#     r1 = requests.get("http://api.brainshop.ai/get?bid=154159&key=8AUfCxCOwuyKOaCT",
#                       headers={
#                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"
#                       },
#                       params={
#                           "uid": 154159,
#                           "msg": mymsg
#                       }
#                       )
#     r2 = json.loads(r1.text)
#     cc = OpenCC("s2tw")
#     # print(cc.convert(r2['cnt']))
#     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cc.convert(r2['cnt'])))