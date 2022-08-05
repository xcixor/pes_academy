# Generated by Django 3.2.13 on 2022-08-05 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_alter_application_expected_max_score'),
        ('agripitch', '0004_auto_20220805_1449'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcriteriaitemdocumentresponse',
            options={'verbose_name_plural': '5 Documents'},
        ),
        migrations.AlterModelOptions(
            name='subcriteriaitemresponse',
            options={'verbose_name_plural': '4 Responses'},
        ),
        migrations.AddField(
            model_name='subcriteriaitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='subcriteriaitemdocumentresponse',
            unique_together={('sub_criteria_item', 'application')},
        ),
    ]
