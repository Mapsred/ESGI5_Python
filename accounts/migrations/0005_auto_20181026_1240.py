# Generated by Django 2.1.2 on 2018-10-26 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20181010_0852'),
        ('accounts', '0004_playercards'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlayerCards',
            new_name='PlayerCard',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='cards',
        ),
    ]
