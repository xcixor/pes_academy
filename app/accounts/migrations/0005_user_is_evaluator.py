# Generated by Django 3.2.13 on 2022-11-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_evaluator',
            field=models.BooleanField(default=False),
        ),
    ]
