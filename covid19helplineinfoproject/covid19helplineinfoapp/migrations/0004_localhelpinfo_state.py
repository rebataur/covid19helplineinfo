# Generated by Django 3.0.4 on 2020-03-22 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19helplineinfoapp', '0003_auto_20200322_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='localhelpinfo',
            name='state',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
    ]
