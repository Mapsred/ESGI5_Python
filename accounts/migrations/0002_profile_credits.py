# Generated by Django 2.1.1 on 2018-09-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='credits',
            field=models.IntegerField(default=200),
        ),
    ]
