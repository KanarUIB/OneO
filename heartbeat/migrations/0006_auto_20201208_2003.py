# Generated by Django 3.1.3 on 2020-12-08 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heartbeat', '0005_auto_20201204_2302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='heartbeat',
            old_name='datum_utc',
            new_name='datum',
        ),
    ]
