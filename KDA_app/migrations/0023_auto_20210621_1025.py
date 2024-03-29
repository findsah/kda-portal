# Generated by Django 3.2.4 on 2021-06-21 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0022_auto_20210621_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availability',
            name='available_time_from',
        ),
        migrations.RemoveField(
            model_name='availability',
            name='available_time_to',
        ),
        migrations.RemoveField(
            model_name='availability',
            name='day',
        ),
        migrations.RemoveField(
            model_name='person',
            name='availability',
        ),
        migrations.AddField(
            model_name='availability',
            name='f_available_time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='f_available_time_to',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='m_available_time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='m_available_time_to',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='psychologist',
            field=models.ForeignKey(default='6', on_delete=django.db.models.deletion.CASCADE, to='KDA_app.person'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='availability',
            name='sa_available_time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='sa_available_time_to',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='su_available_time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='su_available_time_to',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='th_available_time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='th_available_time_to',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='tu_available_time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='tu_available_time_to',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='w_available_time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='w_available_time_to',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
