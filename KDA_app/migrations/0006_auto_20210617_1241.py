# Generated by Django 3.2.4 on 2021-06-17 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0005_auto_20210617_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KDA_app.address'),
        ),
        migrations.AlterField(
            model_name='person',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KDA_app.contact'),
        ),
        migrations.AlterField(
            model_name='person',
            name='hosted_centre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KDA_app.hosted_centre'),
        ),
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KDA_app.role'),
        ),
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KDA_app.status'),
        ),
    ]
