from django.forms import ModelForm
from user.models import User_type

# Create the form class.

from django.forms import ModelForm
from user.models import  User_type


# Create the form class.



class liff(ModelForm):
    class Meta:
        model = User_type
        fields = ['uid',
                  'name',
                  'height',
                  'weight',
                  'age',
                  ]

        labels = {
            'uid': ('uid'),
            'name': ('名稱'),
            'height': ('身高'),
            'weight': ('體重'),
            'age': ('年紀'),
        }



'''
或是可以使用 fields= '__all__' 來指定全部的欄位都須包含。
'''