# Generated by Django 3.2.4 on 2021-06-22 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0028_auto_20210622_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
