# Django_line_bot_basic

### 使用Djagno 建立基本lineBot 範本練習筆記

### Django安裝步驟
1. mkdir xxx    <font color=#FF6600>> 建立資料夾，xxx為資料夾名稱</font>
2. cd xxx <font color=#FF6600>>  切換至該資料夾</font>
3. python3 -m venv xxx_venv <font color=#FF6600>>   安裝虛擬環境</font>
4. source xxx_venv/bin/activate   <font color=#FF6600>>  啟用venv</font>
5. pip3 install django   <font color=#FF6600>>  安裝django</font>
6. django-admin startproject zzz  <font color=#FF6600>>  建立一個專案 ，zzz為專案名</font>
7. 進入zzz/settings.py ，將 LANGUAGE_CODE = 'en-us' 、TIME_ZONE = 'UTC'  
   改成 TIME_ZONE = 'Asia/Taipei'、LANGUAGE_CODE = 'zh-hant'：
8. run cmd > python3 manage.py runserver 






