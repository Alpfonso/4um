# Generated by Django 3.1.6 on 2021-04-01 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum_threads', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Threads',
            new_name='Thread',
        ),
    ]
