# Generated by Django 4.0.3 on 2022-03-12 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_reviewer',
            field=models.BooleanField(default=False),
        ),
    ]
