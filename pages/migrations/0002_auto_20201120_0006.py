# Generated by Django 3.1.3 on 2020-11-19 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kundehatsoftware',
            old_name='swId',
            new_name='software',
        ),
        migrations.RenameField(
            model_name='software',
            old_name='software',
            new_name='software_name',
        ),
    ]
