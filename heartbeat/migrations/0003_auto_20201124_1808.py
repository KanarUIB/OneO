# Generated by Django 3.1.3 on 2020-11-24 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heartbeat', '0002_auto_20201124_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heartbeat',
            name='datum',
            field=models.DateTimeField(),
        ),
    ]
