# Generated by Django 4.0.3 on 2022-03-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_applicationdocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='eligibility',
            field=models.BooleanField(default=False),
        ),
    ]
