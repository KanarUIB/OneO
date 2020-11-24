# Generated by Django 3.1.3 on 2020-11-19 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heartbeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meldung', models.TextField()),
                ('datum', models.DateTimeField()),
                ('kundeSoftware', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.kundehatsoftware')),
            ],
        ),
    ]