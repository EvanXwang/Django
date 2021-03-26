from django.contrib import admin
from user.models import *

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class User_type_Admin(ImportExportModelAdmin):
    list_display = ('uid', 'name', 'height', 'weight', 'age', 'bmi',
                    'sex', 'ac', 'sc', 'bee', 'total_energy', 'pr', 'fat', 'Carb')
admin.site.register(User_type,User_type_Admin)



class Food_Admin(ImportExportModelAdmin):
    list_display = ('en_name', 'tc_name', 'meal', 'cat', 'cal', 'carb', 'pr', 'fat' )
admin.site.register(Food,Food_Admin)


class User_eat_Admin(ImportExportModelAdmin):
    list_display = ('uid', 'name','en_name', 'tc_name', 'cal', 'pr', 'fat', 'carb', 'created_date')
admin.site.register(User_eat,User_eat_Admin)





