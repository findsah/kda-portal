# Generated by Django 3.2.4 on 2021-06-18 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0008_hosted_centres'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hosted_centres',
            old_name='email',
            new_name='spoc_email',
        ),
        migrations.RenameField(
            model_name='hosted_centres',
            old_name='extension_number',
            new_name='spoc_extension_number',
        ),
        migrations.RenameField(
            model_name='hosted_centres',
            old_name='mobile_number',
            new_name='spoc_mobile_number',
        ),
        migrations.RenameField(
            model_name='hosted_centres',
            old_name='office_number',
            new_name='spoc_office_number',
        ),
        migrations.AddField(
            model_name='hosted_centres',
            name='centre_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='hosted_centres',
            name='centre_extension_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hosted_centres',
            name='centre_mobile_number_1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hosted_centres',
            name='centre_mobile_number_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hosted_centres',
            name='centre_office_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hosted_centres',
            name='centre_web_address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]