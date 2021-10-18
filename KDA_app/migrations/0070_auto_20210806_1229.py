# Generated by Django 3.2.4 on 2021-08-06 07:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0069_person_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='sub_test_name',
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='date_last_assessment',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 6), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_1',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 6), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_2',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 6), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_3',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 6), null=True),
        ),
    ]