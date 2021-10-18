# Generated by Django 3.2.4 on 2021-08-30 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0091_auto_20210830_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade_English',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(blank=True, choices=[('mastery', 'Mastery'), ('n_mastery', 'Not Mastered')], max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='skill_english',
            name='a_intervention',
        ),
        migrations.AddField(
            model_name='all_intervention',
            name='skill',
            field=models.ManyToManyField(related_name='a_intervention', to='KDA_app.Skill_English'),
        ),
        migrations.RemoveField(
            model_name='skill_english',
            name='grade',
        ),
        migrations.AddField(
            model_name='skill_english',
            name='grade',
            field=models.ManyToManyField(related_name='skill_english', to='KDA_app.Grade_English'),
        ),
    ]