# Generated by Django 3.2.13 on 2023-02-19 06:50

import common.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, unique=True)),
                ('image', models.FileField(upload_to=common.models.partner_logo_directory_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('for_footer', models.BooleanField(default=False)),
                ('position', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': '6 Partner Logos',
                'ordering': ['position'],
            },
        ),
    ]