# Generated by Django 3.2.13 on 2022-11-07 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0037_scoring_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoring',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]