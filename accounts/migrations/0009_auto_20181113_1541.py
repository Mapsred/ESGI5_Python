# Generated by Django 2.1.2 on 2018-11-13 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20181113_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deckcard',
            old_name='cardPlayer',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='playercard',
            old_name='cardPlayer',
            new_name='card',
        ),
    ]
