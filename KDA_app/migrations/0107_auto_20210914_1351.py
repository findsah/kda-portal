# Generated by Django 3.2.4 on 2021-09-14 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0106_auto_20210914_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child_case_data',
            name='f_phone',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='g_phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='m_phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]