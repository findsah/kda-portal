# Generated by Django 3.2.4 on 2021-08-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0075_auto_20210821_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment_psy',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
