# Generated by Django 3.2.4 on 2021-09-07 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0103_auto_20210907_1615'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homeworks',
            old_name='homeworks',
            new_name='file',
        ),
    ]
