# Generated by Django 2.0.7 on 2018-07-24 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0014_auto_20180724_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='followers',
        ),
    ]