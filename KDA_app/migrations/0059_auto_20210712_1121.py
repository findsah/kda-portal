# Generated by Django 3.2.4 on 2021-07-12 06:21

import KDA_app.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0058_alter_person_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='register_id',
            field=models.ImageField(blank=True, null=True, upload_to=KDA_app.models.Person.get_upload_path_id),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='date_last_assessment',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 12), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_1',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 12), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_2',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 12), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_3',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 12), null=True),
        ),
    ]