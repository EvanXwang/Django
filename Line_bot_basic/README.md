# Django_line_bot_basic

### 使用Djagno 建立基本lineBot 範本練習筆記
### line_bot 自動回聲機器人

### 1. Django安裝步驟
1. mkdir xxx    <font color=#FF6600>> 建立資料夾，xxx為資料夾名稱</font>
2. cd xxx <font color=#FF6600>>  切換至該資料夾</font>
3. python3 -m venv xxx_venv <font color=#FF6600>>   安裝虛擬環境</font>
4. source xxx_venv/bin/activate   <font color=#FF6600>>  啟用venv</font>
5. pip3 install django   <font color=#FF6600>>  安裝django</font>
6. django-admin startproject zzz  <font color=#FF6600>>  建立一個專案 ，zzz為專案名</font>
7. 進入zzz/settings.py ，將 LANGUAGE_CODE = 'en-us' 、TIME_ZONE = 'UTC'  
   改成 TIME_ZONE = 'Asia/Taipei'、LANGUAGE_CODE = 'zh-hant'：
8. run cmd > python3 manage.py runserver 


### 2. Line_bot_basic 建立步驟

1. pip3 install flask
2. pip3 install line_bot_sdk
3. pip3 install liffpy



### 3. settings.py中  輸入自己的Linebot相關資訊
LINE_CHANNEL_ACCESS_TOKEN = ''   
LINE_CHANNEL_SECRET = ''





### 4. line_bot 設定畫面
本地端測試 - 使用ngork  
<img src="https://i.imgur.com/lByiC5L.png" width="50%" />

line管理畫面 - 更改回應設定如下圖：  
<img src="https://i.imgur.com/JDYA0Hq.png" width="70%" />



