# Generated by Django 2.1.1 on 2018-09-24 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('core', '0004_auto_20180921_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('credits', models.IntegerField(default=200)),
            ],
        ),
        migrations.AlterField(
            model_name='card',
            name='attack',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='card',
            name='health',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='deck',
            name='cards',
            field=models.ManyToManyField(to='core.Card'),
        ),
        migrations.AddField(
            model_name='deck',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
    ]
