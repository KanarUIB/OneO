# Generated by Django 3.1.2 on 2020-10-23 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kunde',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandant', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('software', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='KundeHatSoftware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kdNr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.kunde')),
                ('swId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.software')),
            ],
        ),
        migrations.AddField(
            model_name='kunde',
            name='software',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.software'),
        ),
    ]
