# Generated by Django 3.0.4 on 2020-03-22 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19helplineinfoapp', '0004_localhelpinfo_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localhelpinfo',
            old_name='helpline_phonenumber',
            new_name='helpline_phonenumber1',
        ),
        migrations.AddField(
            model_name='localhelpinfo',
            name='helpline_phonenumber2',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='localhelpinfo',
            name='helpline_phonenumber3',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='localhelpinfo',
            name='helpline_whatsapp_phonenumber',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
