# Generated by Django 3.0.4 on 2020-03-22 05:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('profile_pic', models.ImageField(default='/media/profile_pics/placeholder_profile_pic.png', upload_to='profile_pics/')),
                ('address', models.CharField(blank=True, max_length=300)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('country', models.CharField(blank=True, max_length=30)),
                ('zip_code', models.IntegerField(blank=True, default=0, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
