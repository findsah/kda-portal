# Generated by Django 3.2.4 on 2021-06-17 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0003_auto_20210617_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='web_address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]