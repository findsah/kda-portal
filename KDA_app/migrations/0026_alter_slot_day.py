# Generated by Django 3.2.4 on 2021-06-21 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0025_auto_20210621_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='day',
            field=models.DateField(),
        ),
    ]