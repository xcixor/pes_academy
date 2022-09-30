# Generated by Django 3.2.13 on 2022-08-31 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0013_alter_subcriteriaitem_type'),
        ('application', '0004_auto_20220831_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationscore',
            name='question_position',
        ),
        migrations.AlterField(
            model_name='applicationscore',
            name='prompt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='agripitch.subcriteriaitem'),
        ),
    ]