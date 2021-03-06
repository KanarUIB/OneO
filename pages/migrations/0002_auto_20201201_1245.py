# Generated by Django 3.1.3 on 2020-12-01 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ansprechpartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vorname', models.CharField(max_length=100)),
                ('nachname', models.CharField(max_length=100)),
                ('telefon_nr', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RenameField(
            model_name='kunde',
            old_name='mandant',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='kundehatsoftware',
            old_name='swId',
            new_name='software',
        ),
        migrations.RenameField(
            model_name='lizenz',
            old_name='datum_bis',
            new_name='gültig_bis',
        ),
        migrations.RenameField(
            model_name='lizenz',
            old_name='datum_von',
            new_name='gültig_von',
        ),
        migrations.RenameField(
            model_name='software',
            old_name='software',
            new_name='software_name',
        ),
        migrations.RenameField(
            model_name='standort',
            old_name='kunde_ID',
            new_name='kunde',
        ),
        migrations.AddField(
            model_name='kunde',
            name='vf_nummer',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Zuständigkeit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ansprechpartner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.ansprechpartner')),
                ('software', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.software')),
            ],
        ),
        migrations.AddField(
            model_name='ansprechpartner',
            name='standort',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.standort'),
        ),
        migrations.AddField(
            model_name='ansprechpartner',
            name='zuständige_software',
            field=models.ManyToManyField(through='pages.Zuständigkeit', to='pages.Software'),
        ),
    ]
