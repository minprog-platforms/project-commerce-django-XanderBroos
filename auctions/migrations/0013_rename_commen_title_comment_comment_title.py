# Generated by Django 4.1.3 on 2022-11-20 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_bid_title_item_alter_comment_commen_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='commen_title',
            new_name='comment_title',
        ),
    ]