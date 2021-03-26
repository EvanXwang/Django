from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from flask import Flask, request, abort

from linebot.models import *
from user.models import User_type, Food, User_eat
from django.views.generic.base import TemplateView
from django.views.generic import TemplateView
import re

from user.forms import  liff

# Create your views here.

from import_export import resources


class PersonResource(resources.ModelResource):
    class Meta:
        model = Food


def liff2(request):   # liff form 寫入資料庫
    template_name = 'user/User_data.html'
    form = liff(request.POST or None)

    '''
    ■熱量公式：
    常用 Harris Benedict Equation 計算基礎熱量消耗量(BEE)
   
    男BEE(kcal/day)=66+(13.8*weight)+(5*height)-(6.8*age)
    女BEE(kcal/day)=655+(9.6*weight)+(1.8*height)-(4.7*age)
    W:體重 H:身高 A:年齡
    
    ■所需能量= BEE(Basal EnergyExpenditure:BEE)  x 活動因子 x 壓力因子
    '''

    if form.is_valid():

        uid = form.cleaned_data.get('uid')
        name = form.cleaned_data.get('name')
        height = form.cleaned_data.get('height')
        weight = form.cleaned_data.get('weight')
        age = form.cleaned_data.get('age')
        sex = request.POST.getlist('sex') # option 取出後為list > sex[0] 取第0筆
        ac = request.POST.getlist('ac')  # 活動因子option 取出後為list > tmp1[0] 取第0筆
        sc = request.POST.getlist('sc')  # 壓力因子option 取出後為list > tmp2[0] 取第0筆  > 改飲食目標
        bmi = round(weight / ((height / 100) ** 2), 2)

        def createdata(a):
            userlist = User_type.objects.filter(uid=a )  # 搜尋相同欄位資料存成 userlist

            if userlist.exists() == False: # 如果ID不存在則建立資料
                User_type.objects.create(uid=uid, name=name, height=height, weight=weight,
                                             age=age, bmi=bmi, ac=ac[0], sc=sc[0], bee=bee,
                                             sex=sex[0], total_energy=total_energy, pr=pr, fat=fat, Carb=Carb)

            else: # 如果ID存在則修改資料
                userlist.update(uid=uid, name=name, height=height, weight=weight,
                                             age=age, bmi=bmi, ac=ac[0], sc=sc[0], bee=bee,
                                             sex=sex[0], total_energy=total_energy, pr=pr, fat=fat, Carb=Carb)
        #a=bee , b=活動因子, c=飲食目標
        def pr_answer(a,b,c):
            if c == 1.0:
                if b == 1.2:
                    pr = (a * 1.2 * 0.15) / 4
                elif b == 1.375:
                    pr = (a * 1.375 * 0.175) / 4
                elif b == 1.55:
                    pr = (a * 1.55 * 0.175) / 4
                elif b == 1.725:
                    pr = (a * 1.725 * 0.225) / 4
                else:
                    pr = (a * 1.9 * 0.25) / 4
            elif c == 1.2:
                if b == 1.2:
                    pr = (a * 1.2 * 1.2 * 0.15) / 4
                elif b == 1.375:
                    pr = (a * 1.2 * 1.375 * 0.175) / 4
                elif b == 1.55:
                    pr = (a * 1.2 * 1.55 * 0.175) / 4
                elif b == 1.725:
                    pr = (a * 1.2 * 1.725 * 0.225) / 4
                else:
                    pr = (a * 1.2 * 1.9 * 0.25) / 4
            else :
                if b == 1.2:
                    pr = (a * 0.8 * 1.2 * 0.15) / 4
                elif b == 1.375:
                    pr = (a * 0.8 * 1.375 * 0.175) / 4
                elif b == 1.55:
                    pr = (a * 0.8 * 1.55 * 0.175) / 4
                elif b == 1.725:
                    pr = (a * 0.8 * 1.725 * 0.225) / 4
                else:
                    pr = (a * 0.8 * 1.9 * 0.25) / 4
            return pr
        def fat_answer(a,b,c):

            if c == 1.0 :
                if b == 1.2:
                    fat = (a * 1.2 * 0.35) / 9
                elif b == 1.375:
                    fat = (a * 1.375 * 0.325) / 9
                elif b == 1.55:
                    fat = (a * 1.55 * 0.3) / 9
                elif b == 1.725:
                    fat = (a * 1.725 * 0.275) / 9
                else:
                    fat = (a * 1.9 * 0.25) / 9
            elif c == 1.2 :
                if b == 1.2:
                    fat = (a * 1.2 * 1.2 * 0.35) / 9
                elif b == 1.375:
                    fat = (a * 1.2 * 1.375 * 0.325) / 9
                elif b == 1.55:
                    fat = (a * 1.2 * 1.55 * 0.3) / 9
                elif b == 1.725:
                    fat = (a * 1.2 * 1.725 * 0.275) / 9
                else:
                    fat = (a * 1.2 * 1.9 * 0.25) / 9
            else :
                if b == 1.2:
                    fat = (a * 0.8 * 1.2 * 1.2 * 0.35) / 9
                elif b == 1.375:
                    fat = (a * 0.8 * 1.2 * 1.375 * 0.325) / 9
                elif b == 1.55:
                    fat = (a * 0.8 * 1.2 * 1.55 * 0.3) / 9
                elif b == 1.725:
                    fat = (a * 0.8 * 1.2 * 1.725 * 0.275) / 9
                else:
                    fat = (a * 0.8 * 1.2 * 1.9 * 0.25) / 9
            return fat
        def carb_answer(a,b,c):
            if c == 1.0 :
                if b == 1.2:
                    Carb = (a * 1.2 * 0.50) / 4
                elif b == 1.375:
                    Carb = (a * 1.375 * 0.50) / 4
                elif b == 1.55:
                    Carb = (a * 1.55 * 0.50) / 4
                elif b == 1.725:
                    Carb = (a * 1.725 * 0.50) / 4
                else:
                    Carb = (a * 1.9 * 0.50) / 4
            elif c == 1.2 :
                if b == 1.2:
                    Carb = (a * 1.2 * 1.2 * 0.50) / 4
                elif b == 1.375:
                    Carb = (a * 1.2 * 1.375 * 0.50) / 4
                elif b == 1.55:
                    Carb = (a * 1.2 * 1.55 * 0.50) / 4
                elif b == 1.725:
                    Carb = (a * 1.2 * 1.725 * 0.50) / 4
                else:
                    Carb = (a * 1.2 * 1.9 * 0.50) / 4
            else :
                if b == 1.2:
                    Carb = (a * 0.8 * 1.2 * 1.2 * 0.50) / 4
                elif b == 1.375:
                    Carb = (a * 0.8 * 1.2 * 1.375 * 0.50) / 4
                elif b == 1.55:
                    Carb = (a * 0.8 * 1.2 * 1.55 * 0.50) / 4
                elif b == 1.725:
                    Carb = (a * 0.8 * 1.2 * 1.725 * 0.50) / 4
                else:
                    Carb = (a * 0.8 * 1.2 * 1.9 * 0.50) / 4


            return Carb



        if sex[0] == 'male':
            bee = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)  # 男：熱量公式
            total_energy = round(bee * float(ac[0]) * float(sc[0]), 2)  # 男性 所需熱量
            pr = round(pr_answer(bee,float(ac[0]),float(sc[0])),2)
            fat = round(fat_answer(bee,float(ac[0]),float(sc[0])),2)
            Carb = round(carb_answer(bee,float(ac[0]),float(sc[0])),2)
            createdata(uid)
        else :
            bee = 655 +(9.6 * weight)+(1.8 * height)-(4.7 * age)  # 女：熱量公式
            total_energy = round(bee * float(ac[0]) * float(sc[0]), 2)  # 女性 所需熱量
            pr = round(pr_answer(bee, float(ac[0]), float(sc[0])), 2)
            fat = round(fat_answer(bee, float(ac[0]), float(sc[0])), 2)
            Carb = round(carb_answer(bee, float(ac[0]), float(sc[0])), 2)
            createdata(uid)




        return HttpResponse()
    return render(request, template_name, context={'form':form})



def liff3(request):
    users = User_eat.objects.all()


    template_name = 'user/曲線圖-3.html'
    return render(request, template_name, {'users': users}) # notice here we are adding our context to be used in template, you need pass it explicitly








