# Generated by Django 3.0.4 on 2020-04-08 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20200407_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturehalls',
            name='sender_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='account.userProfile'),
        ),
    ]
