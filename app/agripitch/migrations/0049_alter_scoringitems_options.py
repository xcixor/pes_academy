# Generated by Django 3.2.13 on 2022-11-14 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0048_alter_scoringitems_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scoringitems',
            options={'ordering': ['scale'], 'verbose_name_plural': '12. Scoring Items'},
        ),
    ]