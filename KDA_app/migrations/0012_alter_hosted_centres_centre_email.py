# Generated by Django 3.2.4 on 2021-06-18 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0011_hosted_centres_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hosted_centres',
            name='centre_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]