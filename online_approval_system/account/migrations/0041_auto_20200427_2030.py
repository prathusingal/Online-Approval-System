# Generated by Django 3.0.3 on 2020-04-27 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0040_auto_20200427_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dream',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='hobbie1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='hobbie2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='hobbie3',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='hobbie4',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='status',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='thing1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='thing2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='thing3',
        ),
    ]
