# Generated by Django 3.2 on 2021-05-04 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_threads', '0012_auto_20210430_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='score',
            field=models.IntegerField(default=1),
        ),
    ]
