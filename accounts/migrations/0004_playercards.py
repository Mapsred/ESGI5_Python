# Generated by Django 2.1.2 on 2018-10-26 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20181010_0852'),
        ('accounts', '0003_auto_20181010_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbercards', models.IntegerField(default=0)),
                ('cardPlayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Card')),
                ('profilePlayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
    ]
