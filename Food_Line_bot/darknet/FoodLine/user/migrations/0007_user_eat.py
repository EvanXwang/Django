# Generated by Django 3.1.4 on 2021-01-15 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210115_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_eat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='', max_length=50)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('cal', models.FloatField(blank=True, null=True)),
                ('pr', models.FloatField(blank=True, null=True)),
                ('fat', models.FloatField(blank=True, null=True)),
                ('carb', models.FloatField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
