# Generated by Django 3.2.13 on 2022-09-30 13:08

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_application_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselimage',
            name='caption',
            field=ckeditor.fields.RichTextField(),
        ),
    ]