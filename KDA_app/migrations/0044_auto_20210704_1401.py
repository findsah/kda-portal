# Generated by Django 3.2.4 on 2021-07-04 09:01

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0043_alter_pre_evaluation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation_regular',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 4, 9, 1, 49, 569799, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='skill',
            name='pre_eva',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skill_pre', to='KDA_app.pre_evaluation'),
        ),
    ]