# Generated by Django 4.2.14 on 2024-07-31 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('strategicbi', '0009_remove_datamodel_catagory_datamodel_catagory'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stateCode', models.IntegerField(blank=True, default=-1, null=True)),
                ('districtCode', models.IntegerField(blank=True, default=-1, null=True)),
                ('subdistrictCode', models.IntegerField(blank=True, default=-1, null=True)),
                ('villageCode', models.IntegerField(blank=True, default=-1, null=True)),
                ('count', models.IntegerField(blank=True, default=0, null=True)),
                ('catagory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='strategicbi.catagorymodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
