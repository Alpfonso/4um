# Generated by Django 3.1.6 on 2021-04-02 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_threads', '0004_auto_20210402_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
