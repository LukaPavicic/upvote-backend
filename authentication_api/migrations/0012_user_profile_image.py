# Generated by Django 2.2.4 on 2019-10-14 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_api', '0011_auto_20191014_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.FileField(default='', upload_to=''),
        ),
    ]
