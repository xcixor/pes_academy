# Generated by Django 3.2.13 on 2022-09-13 02:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0019_auto_20220913_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcriteriaitemresponse',
            name='list_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), size=None), blank=True, null=True, size=None),
        ),
    ]