# Generated by Django 3.2.1 on 2022-01-27 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_user_is_transcriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessorganization',
            name='facebook_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='businessorganization',
            name='instagram_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='businessorganization',
            name='linkedin_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='businessorganization',
            name='twitter_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='businessorganization',
            name='whatsapp_business_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
