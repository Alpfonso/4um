# Generated by Django 3.2 on 2021-04-26 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum_threads', '0010_rename_thread_comments_thread_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread_comment',
            name='parent_thread',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='forum_threads.thread'),
            preserve_default=False,
        ),
    ]
