# Generated by Django 3.2.4 on 2021-07-03 19:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0040_alter_intervention_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child_case_data',
            name='date_last_assessment',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 3), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_1',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 3), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_2',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 3), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_3',
            field=models.DateField(blank=True, default=datetime.date(2021, 7, 3), null=True),
        ),
        migrations.CreateModel(
            name='Assessment_psy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=300)),
                ('sub_test_name', models.CharField(max_length=300)),
                ('sub_score', models.IntegerField()),
                ('sub_time', models.TimeField()),
                ('sub_grade', models.CharField(max_length=300)),
                ('test_date', models.DateField()),
                ('cognitive_date', models.DateField()),
                ('cognitive_result', models.CharField(max_length=300)),
                ('recommendations', models.CharField(max_length=300)),
                ('notice', models.CharField(max_length=300)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assess2', to=settings.AUTH_USER_MODEL)),
                ('psychologist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assess1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
