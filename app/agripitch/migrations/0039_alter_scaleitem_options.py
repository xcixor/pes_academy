# Generated by Django 3.2.13 on 2022-11-07 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0038_alter_scoring_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scaleitem',
            options={'ordering': ['score'], 'verbose_name_plural': '9. Scale Items'},
        ),
    ]