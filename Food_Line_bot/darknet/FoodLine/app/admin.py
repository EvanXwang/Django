from django.contrib import admin

# Register your models here.
from app.models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'pic_url', 'mtext', 'mdt')
admin.site.register(User_Info,User_Info_Admin)


class Jobs_Admin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'job_name', 'percentage', 'description', 'mdt')
admin.site.register(Jobs,Jobs_Admin)
