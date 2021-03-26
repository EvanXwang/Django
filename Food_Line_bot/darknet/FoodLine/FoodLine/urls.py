"""FoodLine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include  #Django 2.0 專案預設建立的檔案架構
from django.conf.urls import url  #Django 1.X 的語法
from app.views import callback
from user.views import  liff,  liff2, liff3

'''
說明連結：http://blog.e-happy.com.tw/django2-0-%E4%BB%A5-path-
%E5%87%BD%E5%BC%8F%E8%A8%AD%E5%AE%9A-urlpatterns/

Django 1.X 使用的 URL routing 語法，是以 regular expression 傳遞參數。
這部分在 Django 2.0 當中改掉了，以前會把 url routing 這樣寫：
url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),

Django 2.0 預設的 path 方法，是採用更簡單的 URL 路由語法傳遞參數。語法如下：
path(url, view, name=None)

'''

urlpatterns = [

    path('admin/', admin.site.urls),
    url('^callback', callback),
    url('^liff',liff2),#新增liff這個url，這個是用來建例LIFF轉跳頁面用的
    url('^test',liff3),# test 網址路徑 、 liff3  funtion名稱




]

