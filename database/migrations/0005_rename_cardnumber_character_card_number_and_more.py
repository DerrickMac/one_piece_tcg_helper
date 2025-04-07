# Generated by Django 5.2 on 2025-04-07 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_remove_pricehistory_database_pr_content_a45df8_idx_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='character',
            old_name='cardNumber',
            new_name='card_number',
        ),
        migrations.RenameField(
            model_name='character',
            old_name='colorOne',
            new_name='color_one',
        ),
        migrations.RenameField(
            model_name='character',
            old_name='colorTwo',
            new_name='color_two',
        ),
        migrations.RenameField(
            model_name='character',
            old_name='imageUrl',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='character',
            old_name='lastUpdated',
            new_name='last_updated',
        ),
        migrations.RenameField(
            model_name='character',
            old_name='productId',
            new_name='product_id',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='cardNumber',
            new_name='card_number',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='colorOne',
            new_name='color_one',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='colorTwo',
            new_name='color_two',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='imageUrl',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='lastUpdated',
            new_name='last_updated',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='productId',
            new_name='product_id',
        ),
        migrations.RenameField(
            model_name='leader',
            old_name='cardNumber',
            new_name='card_number',
        ),
        migrations.RenameField(
            model_name='leader',
            old_name='colorOne',
            new_name='color_one',
        ),
        migrations.RenameField(
            model_name='leader',
            old_name='colorTwo',
            new_name='color_two',
        ),
        migrations.RenameField(
            model_name='leader',
            old_name='imageUrl',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='leader',
            old_name='lastUpdated',
            new_name='last_updated',
        ),
        migrations.RenameField(
            model_name='leader',
            old_name='productId',
            new_name='product_id',
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='cardNumber',
            new_name='card_number',
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='colorOne',
            new_name='color_one',
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='colorTwo',
            new_name='color_two',
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='imageUrl',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='lastUpdated',
            new_name='last_updated',
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='productId',
            new_name='product_id',
        ),
    ]
