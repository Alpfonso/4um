# Generated by Django 3.2 on 2021-05-24 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_threads', '0015_thread_live_thread_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='thread_summary',
            field=models.TextField(blank=True),
        ),
    ]