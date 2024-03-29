# Generated by Django 3.2.4 on 2021-08-21 12:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0074_person_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill_arabic',
            name='n_eight',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_eleven',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_five',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_four',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_nine',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_one',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_seven',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_six',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_ten',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_three',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='skill_arabic',
            name='n_two',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='date_last_assessment',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 21), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_1',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 21), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_2',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 21), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_3',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 21), null=True),
        ),
    ]
