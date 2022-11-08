# Generated by Django 3.2.13 on 2022-11-05 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0035_remove_scale_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scoring', to='agripitch.subcriteriaitem')),
                ('scale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scoring', to='agripitch.scale')),
            ],
            options={
                'verbose_name_plural': '10. Scoring',
            },
        ),
    ]