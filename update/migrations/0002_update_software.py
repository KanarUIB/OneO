# Generated by Django 3.1.2 on 2021-01-06 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_kundenlizenz_standortlizenz'),
        ('update', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='software',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pages.software'),
        ),
    ]