# Generated by Django 3.2.4 on 2021-08-27 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0086_auto_20210827_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation_regular',
            name='date',
        ),
    ]
