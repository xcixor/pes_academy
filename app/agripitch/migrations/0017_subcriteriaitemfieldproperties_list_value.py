# Generated by Django 3.2.13 on 2022-09-13 01:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0016_alter_subcriteriaitemfieldproperties_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcriteriaitemfieldproperties',
            name='list_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), size=8), blank=True, null=True, size=8),
        ),
    ]
