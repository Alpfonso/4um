# Generated by Django 3.1.6 on 2021-04-02 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_threads', '0005_auto_20210402_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='sticky_thread',
            field=models.BooleanField(default=False),
        ),
    ]