# Generated by Django 3.2.13 on 2022-07-20 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortlist',
            name='afdb_application',
        ),
    ]
