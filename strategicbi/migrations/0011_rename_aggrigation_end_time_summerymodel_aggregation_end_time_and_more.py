# Generated by Django 4.2.14 on 2024-08-22 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strategicbi', '0010_summerymodel_aggrigation_end_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summerymodel',
            old_name='aggrigation_end_time',
            new_name='aggregation_end_time',
        ),
        migrations.RenameField(
            model_name='summerymodel',
            old_name='aggrigation_start_time',
            new_name='aggregation_start_time',
        ),
        migrations.RenameField(
            model_name='summerymodel',
            old_name='aggrigation_status',
            new_name='aggregation_status',
        ),
    ]
