# Generated by Django 3.2.13 on 2022-11-10 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0044_alter_applicationmarks_scoring'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scaleitem',
            name='scale',
        ),
    ]
