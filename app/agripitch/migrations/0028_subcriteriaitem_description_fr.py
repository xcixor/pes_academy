# Generated by Django 3.2.13 on 2022-10-12 07:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0027_remove_subcriteriaitemchoice_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcriteriaitem',
            name='description_fr',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]