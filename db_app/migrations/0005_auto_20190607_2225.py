# Generated by Django 2.1.7 on 2019-06-07 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db_app', '0004_auto_20190607_2223'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='artist_tags',
            new_name='artist_tag',
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name_plural': 'media'},
        ),
    ]
