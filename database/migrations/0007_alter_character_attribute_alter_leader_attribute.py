# Generated by Django 5.2 on 2025-04-13 04:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_alter_character_color_two_alter_character_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='attribute',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='leader',
            name='attribute',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=None),
        ),
    ]
