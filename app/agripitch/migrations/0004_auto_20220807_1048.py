# Generated by Django 3.2.13 on 2022-08-07 10:48

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0003_auto_20220807_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcriteriaitem',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subcriteriaitem',
            name='label',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='subcriteriaitemchoice',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
