# Generated by Django 3.0.4 on 2020-03-28 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19helplineinfoapp', '0018_profile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localhelpinfo',
            name='state',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
