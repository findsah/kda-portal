# Generated by Django 3.2.4 on 2021-06-27 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0033_alter_child_case_data_age_problem'),
    ]

    operations = [
        migrations.AddField(
            model_name='child_case_data',
            name='punishment',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]