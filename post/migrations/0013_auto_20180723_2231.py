# Generated by Django 2.0.7 on 2018-07-23 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_auto_20180723_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(default='profile_pic/profile_pic.png', upload_to='profile_pic'),
        ),
    ]