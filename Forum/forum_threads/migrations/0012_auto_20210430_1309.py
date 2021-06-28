# Generated by Django 3.2 on 2021-04-30 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_threads', '0011_thread_comment_parent_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='tags',
            field=models.CharField(default=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='thread_comment',
            name='comment_content',
            field=models.TextField(max_length=255),
        ),
    ]
