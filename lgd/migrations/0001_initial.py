# Generated by Django 4.2.14 on 2024-07-25 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('districtCode', models.IntegerField(blank=True, null=True)),
                ('districtNameEnglish', models.CharField(blank=True, max_length=300, null=True)),
                ('districtNameLocal', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stateCode', models.IntegerField(blank=True, null=True)),
                ('stateNameEnglish', models.CharField(blank=True, max_length=300, null=True)),
                ('stateNameLocal', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubDistrictModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subdistrictCode', models.IntegerField(blank=True, null=True)),
                ('subdistrictNameEnglish', models.CharField(blank=True, max_length=300, null=True)),
                ('subdistrictNameLocal', models.CharField(blank=True, max_length=300, null=True)),
                ('districtCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lgd.districtmodel')),
                ('stateCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lgd.statemodel')),
            ],
        ),
        migrations.CreateModel(
            name='VillageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('villageCode', models.IntegerField(blank=True, null=True)),
                ('villageNameEnglish', models.CharField(blank=True, max_length=300, null=True)),
                ('villageNameLocal', models.CharField(blank=True, max_length=300, null=True)),
                ('districtCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lgd.districtmodel')),
                ('stateCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lgd.statemodel')),
                ('subdistrictCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lgd.subdistrictmodel')),
            ],
        ),
        migrations.AddConstraint(
            model_name='statemodel',
            constraint=models.UniqueConstraint(fields=('stateCode',), name='unique state'),
        ),
        migrations.AddField(
            model_name='districtmodel',
            name='stateCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lgd.statemodel'),
        ),
        migrations.AddConstraint(
            model_name='villagemodel',
            constraint=models.UniqueConstraint(fields=('villageCode',), name='unique village'),
        ),
        migrations.AddConstraint(
            model_name='subdistrictmodel',
            constraint=models.UniqueConstraint(fields=('subdistrictCode',), name='unique subdistrict'),
        ),
        migrations.AddConstraint(
            model_name='districtmodel',
            constraint=models.UniqueConstraint(fields=('districtCode',), name='unique district'),
        ),
    ]
