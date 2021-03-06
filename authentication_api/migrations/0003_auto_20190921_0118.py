# Generated by Django 2.2.4 on 2019-09-20 23:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_api', '0002_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='number_of_members',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='UserJoinedCommunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication_api.Community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
