# Generated by Django 3.0.4 on 2020-03-27 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19helplineinfoapp', '0016_auto_20200327_0552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='seeking_help',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='volunteer',
        ),
        migrations.AddField(
            model_name='profile',
            name='help_type',
            field=models.CharField(choices=[('SEEKING_HELP', 'Seeking Help'), ('VOLUNTEER', 'Volunteer')], max_length=30, null=True),
        ),
    ]
