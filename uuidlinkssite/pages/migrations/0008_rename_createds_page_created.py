# Generated by Django 4.0.4 on 2022-04-13 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_rename_created_page_createds'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='createds',
            new_name='created',
        ),
    ]
