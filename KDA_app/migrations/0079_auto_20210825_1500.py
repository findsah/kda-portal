# Generated by Django 3.2.4 on 2021-08-25 10:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0078_auto_20210824_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment_psy',
            name='appointment',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='assess', to='KDA_app.appointment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cognitive_assessment',
            name='appointment',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='cog', to='KDA_app.appointment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluation_regular',
            name='intervention',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='eva', to='KDA_app.all_intervention'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pre_evaluation',
            name='intervention',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_eva', to='KDA_app.intervention'),
        ),
        migrations.AlterField(
            model_name='availability',
            name='m_available_time_from',
            field=models.TimeField(blank=True, default='08:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='m_available_time_to',
            field=models.TimeField(blank=True, default='20:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='sa_available_time_from',
            field=models.TimeField(blank=True, default='08:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='sa_available_time_to',
            field=models.TimeField(blank=True, default='20:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='su_available_time_from',
            field=models.TimeField(blank=True, default='08:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='su_available_time_to',
            field=models.TimeField(blank=True, default='20:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='th_available_time_from',
            field=models.TimeField(blank=True, default='08:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='th_available_time_to',
            field=models.TimeField(blank=True, default='20:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='tu_available_time_from',
            field=models.TimeField(blank=True, default='08:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='tu_available_time_to',
            field=models.TimeField(blank=True, default='20:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='w_available_time_from',
            field=models.TimeField(blank=True, default='08:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='w_available_time_to',
            field=models.TimeField(blank=True, default='20:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='date_last_assessment',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 25), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_1',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 25), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_2',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 25), null=True),
        ),
        migrations.AlterField(
            model_name='child_case_data',
            name='enroll_date_3',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 25), null=True),
        ),
    ]
