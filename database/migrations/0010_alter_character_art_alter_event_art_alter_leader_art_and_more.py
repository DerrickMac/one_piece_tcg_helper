# Generated by Django 5.2 on 2025-04-14 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_alter_character_card_number_alter_event_card_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='art',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='event',
            name='art',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='leader',
            name='art',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='stage',
            name='art',
            field=models.CharField(max_length=13),
        ),
    ]
