# Generated by Django 3.2.13 on 2022-11-15 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_alter_application_stage'),
        ('agripitch', '0051_applicationmarks_scoring'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='applicationmarks',
            unique_together={('application', 'question', 'scoring')},
        ),
    ]
