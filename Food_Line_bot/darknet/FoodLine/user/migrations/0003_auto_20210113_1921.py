# Generated by Django 3.1.4 on 2021-01-13 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210109_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_type',
            name='Carb',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user_type',
            name='fat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user_type',
            name='protein',
            field=models.FloatField(blank=True, null=True),
        ),
    ]