from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from app.models import *
from user.models import *
import datetime
from datetime import datetime


# 個人資料
def person_data(uid):
    datas = User_type.objects.filter(uid=uid)
    for data in datas:
        name = data.name
        height = str(data.height)
        weight = str(data.weight)
        age = str(data.age)
        sex = data.sex
        bmi = str(data.bmi)
        bee = str(round(data.bee, 2))
        total_energy = str(data.total_energy)

    contents = {
        "type": "carousel",
        "contents": [
            {
                "hero": {
                    "type": "image",
                    "url": "https://riskonnect.com/wp-content/uploads/2019/09/Healthcare-blog2.png",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [

                        {
                            "type": "text",
                            "text": name + "個人基本資料：",  # 可加入一段話說明
                            "weight": "bold",
                            "size": "md",
                            "color": "#1DB446",
                            "wrap": True
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "身高",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": height,
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "體重",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": weight,
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "年紀",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": age,
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },

                                {
                                    "type": "box",
                                    "layout": "horizontal",

                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "性別",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": sex,
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "xxl"
                                },

                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "xxl",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "BMI值",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": bmi,
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "基礎熱量消耗量",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": bee,
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "每日基本所需熱量",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": total_energy,
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": " ",  # 可加入一段話說明
                                    "size": "xs",
                                    "color": "#aaaaaa",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": " ",  # 可加入一段話說明
                                    "color": "#aaaaaa",
                                    "size": "xs",
                                    "align": "end"
                                }
                            ]
                        }
                    ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='FlexMessage範例1', contents=contents)
    return message


# 推薦系統
def recommender_system(b1, b2, l1, l2, l3, l4, d1, d2, d3, d4):
    # 早餐-主食
    datas = Food.objects.filter(tc_name=b1)
    for data in datas:
        cal = data.cal
        carb = data.carb
        pr = data.pr
        fat = data.fat
    # 早餐-飲料
    datas1 = Food.objects.filter(tc_name=b2)
    for data1 in datas1:
        cal1 = data1.cal
        carb1 = data1.carb
        pr1 = data1.pr
        fat1 = data1.fat
    # 中餐-主食
    datas2 = Food.objects.filter(tc_name=l1)
    for data2 in datas2:
        cal2 = data2.cal
        carb2 = data2.carb
        pr2 = data2.pr
        fat2 = data2.fat
    # 中餐-配菜
    datas3 = Food.objects.filter(tc_name=l2)
    for data3 in datas3:
        cal3 = data3.cal
        carb3 = data3.carb
        pr3 = data3.pr
        fat3 = data3.fat
    # 中餐-湯
    datas4 = Food.objects.filter(tc_name=l3)
    for data4 in datas4:
        cal4 = data4.cal
        carb4 = data4.carb
        pr4 = data4.pr
        fat4 = data4.fat
    # 中餐-甜點
    datas5 = Food.objects.filter(tc_name=l4)
    for data5 in datas5:
        cal5 = data5.cal
        carb5 = data5.carb
        pr5 = data5.pr
        fat5 = data5.fat

    # 晚餐-主食
    datas6 = Food.objects.filter(tc_name=d1)
    for data6 in datas6:
        cal6 = data6.cal
        carb6 = data6.carb
        pr6 = data6.pr
        fat6 = data6.fat
    # 晚餐-配菜
    datas7 = Food.objects.filter(tc_name=d2)
    for data7 in datas7:
        cal7 = data7.cal
        carb7 = data7.carb
        pr7 = data7.pr
        fat7 = data7.fat
    # 晚餐-湯
    datas8 = Food.objects.filter(tc_name=d3)
    for data8 in datas8:
        cal8 = data8.cal
        carb8 = data8.carb
        pr8 = data8.pr
        fat8 = data8.fat
    # 晚餐-水果
    datas9 = Food.objects.filter(tc_name=d4)
    for data9 in datas9:
        cal9 = data9.cal
        carb9 = data9.carb
        pr9 = data9.pr
        fat9 = data9.fat

    contents = {
        "type": "carousel",
        "contents": [

            # 早餐
            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": " 今日推薦早餐",
                            "weight": "bold",
                            "align": "center",
                            "size": "xl",
                            "margin": "md"
                        }
                    ]
                },
                "hero": {
                    "type": "image",
                    "url": "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/delicious-breakfast-on-a-light-table-royalty-free-image-863444442-1543345985.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "食物名稱",
                                            "size": "sm",
                                            "color": "#555555",
                                            "weight": "bold",
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": "熱量",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "蛋白質",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "脂質",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "醣類",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },

                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "md"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(b1),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(b2),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal1),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr1),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat1),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb1),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                },

                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "Like",
                                "data": "like",
                                "displayText": "Like!!!"
                            },
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "margin": "sm",
                            "action": {
                                "type": "uri",
                                "label": "food map",
                                "uri": "https://liff.line.me/1655422172-pg9G10bZ"
                            },
                            "style": "secondary"
                        }
                    ]
                }
            },
            # 午餐
            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": " 今日推薦午餐",
                            "weight": "bold",
                            "align": "center",
                            "size": "xl",
                            "margin": "md"
                        }
                    ]
                },
                "hero": {
                    "type": "image",
                    "url": "https://www.cloudland.tv/wp-content/uploads/2019/03/cloudland-italian-restaurant.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "食物名稱",
                                            "size": "sm",
                                            "color": "#555555",
                                            "weight": "bold",
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": "熱量",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "蛋白質",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "脂質",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "醣類",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },

                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "md"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(l1),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal2),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr2),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat2),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb2),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(l2),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal3),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr3),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat3),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb3),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(l3),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal4),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr4),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat4),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb4),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(l4),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal5),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr5),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat5),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb5),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "Like",
                                "data": "SCHEDULE",
                                "displayText": "Schedule"
                            },
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "margin": "sm",
                            "action": {
                                "type": "uri",
                                "label": "Unlike",
                                "uri": "https://sitthi.me:3807/downloaded/dd470058eafc4d0991ef21870505113c.json"
                            },
                            "style": "secondary"
                        }
                    ]
                }
            },
            # 晚餐
            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": " 今日推薦晚餐",
                            "weight": "bold",
                            "align": "center",
                            "size": "xl",
                            "margin": "md"
                        }
                    ]
                },
                "hero": {
                    "type": "image",
                    "url": "https://www.okibook.com/userfiles/promotions/Osteria_Christmas%20set%20dinner%20menu_%E6%84%8F%E5%A4%A7%E5%88%A9%E8%81%96%E8%AA%95%E6%99%9A%E9%A4%90r.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "食物名稱",
                                            "size": "sm",
                                            "color": "#555555",
                                            "weight": "bold",
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": "熱量",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "蛋白質",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "脂質",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": "醣類",
                                            "size": "xs",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        },

                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "md"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(d1),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal6),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr6),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat6),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb6),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(d2),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal7),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr7),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat7),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb7),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(d3),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal8),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr8),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat8),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb8),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [

                                                {
                                                    "type": "text",
                                                    "text": str(d4),
                                                    "size": "sm",
                                                    "color": "#555555"
                                                }
                                            ],
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": str(cal9),
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(pr9),
                                            "size": "sm",
                                            "color": "#00ff00",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(fat9),
                                            "size": "sm",
                                            "color": "#aaaaaa",
                                            "align": "end"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(carb9),
                                            "size": "sm",
                                            "color": "#ff0000",
                                            "align": "end"
                                        },

                                    ]
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "Like",
                                "data": "SCHEDULE",
                                "displayText": "Schedule"
                            },
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "margin": "sm",
                            "action": {
                                "type": "uri",
                                "label": "Unlike",
                                "uri": "https://sitthi.me:3807/downloaded/dd470058eafc4d0991ef21870505113c.json"
                            },
                            "style": "secondary"
                        }
                    ]
                }
            },

        ]
    }
    message = FlexSendMessage(alt_text='FlexMessage範例1', contents=contents)
    return message


# 查詢每日所需營養數值
def person_nutrition(uid):
    def mylist():
        date = datetime.today().date()
        user = User_eat.objects.filter(uid=uid)  # 查詢 自己的id
        times = user.filter(created_date__date=date)  # 使用自己的id  搜尋時間
        cal, pr, fat, carb = 0, 0, 0, 0
        for time in times:  # 依序把資料存成字串
            cal = cal + time.cal
            pr = pr + time.pr
            fat = fat + time.fat
            carb = carb + time.carb
        return cal, pr, fat, carb

    list = mylist()
    my_cal = list[0]
    my_pr = list[1]
    my_fat = list[2]
    my_carb = list[3]

    datas = User_type.objects.filter(uid=uid)
    for data in datas:
        total_energy = data.total_energy
        pr = data.pr
        fat = data.fat
        Carb = data.Carb

    new_my_cal = (my_cal / total_energy) * 100
    new_my_fat = (my_fat / fat) * 100
    new_my_pr = (my_pr / pr) * 100
    new_my_carb = (my_carb / Carb) * 100

    contents = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "nano",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "總熱量",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(total_energy) + '大卡',
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": str(new_my_cal) + "%",
                                    "backgroundColor": "#0D8186",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#9FD8E36E",
                            "height": "6px",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": '目前' + str(round(new_my_cal, 2)) + "%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                    ],
                    "backgroundColor": "#27ACB2",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "(醣類、脂質、蛋白質），經過重重化學反應，最後產生能量及熱量",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": False
                    }
                }
            },
            {
                "type": "bubble",
                "size": "nano",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "脂質",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(fat) + '公克',
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": str(new_my_fat) + "%",
                                    "backgroundColor": "#DE5658",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#FAD2A76E",
                            "height": "6px",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": '目前' + str(round(new_my_fat, 2)) + "%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                    ],
                    "backgroundColor": "#FF6B6E",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "可提供能量和必需脂肪酸",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": False
                    }
                }
            },
            {
                "type": "bubble",
                "size": "nano",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "醣類",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(Carb) + '公克',
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": str(new_my_carb) + "%",
                                    "backgroundColor": "#7D51E4",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#9FD8E36E",
                            "height": "6px",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": '目前' + str(round(new_my_carb, 2)) + "%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                    ],
                    "backgroundColor": "#A17DF5",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "醣類是身體的能量來源，它又稱為「碳水化合物」",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": False
                    }
                }
            },
            {
                "type": "bubble",
                "size": "nano",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "蛋白質",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(pr) + '公克',
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": str(new_my_pr) + "%",
                                    "backgroundColor": "#0D8186",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#9FD8E36E",
                            "height": "6px",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": '目前' + str(round(new_my_pr, 2)) + "%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },

                    ],
                    "backgroundColor": "#27ACB2",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "它們催化生物化學反應，尤其對於生物體的代謝至關重要",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": False
                    }
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='FlexMessage範例1', contents=contents)
    return message


# 將JSON設定為變數content，並以FlexSendMessage()包成Flex Message
def jobs_progress(uid):
    contents = dict()
    contents['type'] = 'carousel'
    bubbles = []
    datas = User_type.objects.filter(uid=uid)
    for data in datas:
        label = "所需熱量"
        percentage = data.total_energy
        text = '標準'
        bubble = {"type": "bubble",
                  "size": "nano",
                  "header": {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [
                          {
                              "type": "text",
                              "text": label,
                              "color": "#ffffff",
                              "align": "start",
                              "size": "md",
                              "gravity": "center"
                          },
                          {
                              "type": "text",
                              "text": str(percentage) + "Cal",
                              "color": "#ffffff",
                              "align": "start",
                              "size": "xs",
                              "gravity": "center",
                              "margin": "lg"
                          },
                          {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                  {
                                      "type": "box",
                                      "layout": "vertical",
                                      "contents": [
                                          {
                                              "type": "filler"
                                          }
                                      ],
                                      "width": str(percentage) + "%",
                                      "backgroundColor": "#0D8186",
                                      "height": "6px"
                                  }
                              ],
                              "backgroundColor": "#9FD8E36E",
                              "height": "6px",
                              "margin": "sm"
                          }
                      ],
                      "backgroundColor": "#27ACB2",
                      "paddingTop": "19px",
                      "paddingAll": "12px",
                      "paddingBottom": "16px"
                  },
                  "body": {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [
                          {
                              "type": "box",
                              "layout": "horizontal",
                              "contents": [
                                  {
                                      "type": "text",
                                      "text": text,
                                      "color": "#8C8C8C",
                                      "size": "sm",
                                      "wrap": True
                                  }
                              ],
                              "flex": 1
                          }
                      ],
                      "spacing": "md",
                      "paddingAll": "12px"
                  },
                  "styles": {
                      "footer": {
                          "separator": False
                      }
                  }
                  }
        bubbles.append(bubble)
    contents['contents'] = bubbles
    message = FlexSendMessage(alt_text='工作進度', contents=contents)
    return message

