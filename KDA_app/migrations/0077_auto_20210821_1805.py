# Generated by Django 3.2.4 on 2021-08-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0076_assessment_psy_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='cognitive_assessment',
            name='history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cognitive_assessment',
            name='cognitive_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cognitive_assessment',
            name='cognitive_result',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cognitive_assessment',
            name='notice',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cognitive_assessment',
            name='recommendations',
            field=models.TextField(blank=True, null=True),
        ),
    ]
