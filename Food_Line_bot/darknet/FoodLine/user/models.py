# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class User_type(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')               # user_id
    name = models.CharField(max_length=255,blank=True,null=False)             # LINE名字
    height = models.FloatField(blank=True)                                    # 身高
    weight = models.FloatField(blank=True)                                    # 體重
    age = models.IntegerField(blank=True)                                     # 年紀
    bmi = models.FloatField(blank=True)                                       # bmi公式
    sex = models.CharField(max_length=20, null=True)                          # 性別
    ac = models.FloatField(blank=True, null=True)                             # 活動因子
    sc = models.FloatField(blank=True, null=True)                             # 壓力因子 > 改 飲食目標
    bee = models.FloatField(blank=True, null=True)                            # 基礎熱量消耗量
    total_energy = models.FloatField(blank=True, null=True)                   # 所需能量
    pr = models.FloatField(blank=True, null=True)  # 蛋白質
    fat = models.FloatField(blank=True, null=True)  # 脂肪
    Carb = models.FloatField(blank=True, null=True)  # 醣類

    def __str__(self):
        return self.uid



# 現有資料庫若要新增欄位，最好後面加 null=True 才不會誤判空值，無法新增

class Food(models.Model):   # 測試寫入form
    en_name  = models.CharField(max_length=100, null=True) # 食物英文名稱
    tc_name = models.CharField(max_length=100, null=True) # 食物中文名稱
    meal = models.CharField(max_length=100, null=True) # 餐類別
    cat = models.CharField(max_length=100, null=True) # 食物類別
    cal = models.FloatField(blank=True, null=True)  # 熱量
    carb = models.FloatField(blank=True, null=True)  # 醣類
    pr = models.FloatField(blank=True, null=True)  # 蛋白質
    fat = models.FloatField(blank=True, null=True)  # 脂肪


# 新增使用者每日 餐點，需另附 時間欄位

class User_eat(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')  # user_id
    name = models.CharField(max_length=255,blank=True,null=False) # LINE名字
    en_name = models.CharField(max_length=100, null=True)
    tc_name = models.CharField(max_length=100, null=True)
    cal = models.FloatField(blank=True, null=True)  # 熱量
    pr = models.FloatField(blank=True, null=True)  # 蛋白質
    fat = models.FloatField(blank=True, null=True)  # 脂肪
    carb = models.FloatField(blank=True, null=True)  # 醣類
    created_date = models.DateTimeField(auto_now_add=True)  # 創建日期

    def __str__(self):
        return self.uid
