# Generated by Django 3.2.13 on 2023-02-19 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_is_evaluator'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='type',
            field=models.CharField(choices=[('psa', 'PSA'), ('support', 'SUPPORT')], default='psa', max_length=100, verbose_name='Type of Coach'),
        ),
    ]