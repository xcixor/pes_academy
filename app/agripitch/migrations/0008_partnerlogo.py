# Generated by Django 3.2.13 on 2022-08-22 08:34

import agripitch.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0007_alter_subcriteriaitemfieldproperties_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.FileField(upload_to=agripitch.models.partner_logo_directory_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField()),
                ('for_footer', models.BooleanField(default=False)),
                ('position', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
