# Generated by Django 3.2.1 on 2022-01-19 10:44

from django.db import migrations, models
import sme.models.application


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=sme.models.application.image_directory_path)),
                ('tagline', models.CharField(help_text='A title for the application.', max_length=255)),
                ('description', models.TextField(help_text='A description of what the application is about.')),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
    ]