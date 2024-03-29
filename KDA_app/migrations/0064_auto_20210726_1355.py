# Generated by Django 3.2.4 on 2021-07-26 08:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0063_assessment_psy_sub_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='nationality',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='date_last_assessment',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 26), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_1',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 26), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_2',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 26), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_3',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 26), null=True),
        ),
    ]
