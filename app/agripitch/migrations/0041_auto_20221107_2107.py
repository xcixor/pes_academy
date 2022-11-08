# Generated by Django 3.2.13 on 2022-11-07 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_alter_application_options'),
        ('agripitch', '0040_auto_20221107_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationmarks',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='application.application'),
        ),
        migrations.AlterField(
            model_name='applicationmarks',
            name='scoring',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoring', to='agripitch.scoring'),
        ),
    ]
