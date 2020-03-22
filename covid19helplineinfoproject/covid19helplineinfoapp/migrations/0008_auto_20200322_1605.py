# Generated by Django 3.0.4 on 2020-03-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19helplineinfoapp', '0007_auto_20200322_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localhelpinfo',
            name='city',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='localhelpinfo',
            name='country',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='localhelpinfo',
            name='helpline_phonenumber1',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='localhelpinfo',
            name='state',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='localhelpinfo',
            unique_together={('city', 'state', 'country')},
        ),
    ]