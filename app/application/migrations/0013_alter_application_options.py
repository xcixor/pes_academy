# Generated by Django 3.2.13 on 2022-10-31 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_alter_application_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['created']},
        ),
    ]