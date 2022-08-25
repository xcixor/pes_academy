# Generated by Django 3.2.13 on 2022-08-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agripitch', '0012_rename_link_partnerlogo_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcriteriaitem',
            name='type',
            field=models.CharField(choices=[('charfield', 'One Line Text'), ('textfield', 'Multiple Line Text'), ('choicefield', 'Dropdown'), ('file', 'File'), ('numberfield', 'Number'), ('radiofield', 'Choice'), ('datefield', 'Date'), ('countryfield', 'Country')], max_length=100),
        ),
    ]
