# Generated by Django 2.1.2 on 2018-10-08 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenIDNonce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_url', models.CharField(max_length=255)),
                ('timestamp', models.IntegerField()),
                ('salt', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpenIDStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_url', models.CharField(max_length=255)),
                ('handle', models.CharField(max_length=255)),
                ('secret', models.TextField()),
                ('issued', models.IntegerField()),
                ('lifetime', models.IntegerField()),
                ('assoc_type', models.TextField()),
            ],
        ),
    ]
