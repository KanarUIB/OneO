# Generated by Django 3.1.3 on 2020-11-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heartbeat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heartbeat',
            name='datum',
            field=models.CharField(max_length=20),
        ),
    ]
