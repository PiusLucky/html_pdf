# Generated by Django 3.0.1 on 2020-03-09 21:34

from django.db import migrations, models
import main.logic


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_year', models.CharField(default=main.logic.current_year, max_length=4, verbose_name='current_year')),
                ('start_year', models.CharField(default=2020, max_length=4, verbose_name='start_year')),
            ],
        ),
    ]
