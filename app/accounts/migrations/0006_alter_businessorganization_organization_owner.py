# Generated by Django 3.2.1 on 2022-02-03 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220203_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessorganization',
            name='organization_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='businesses', to=settings.AUTH_USER_MODEL),
        ),
    ]
