# Generated by Django 3.2 on 2021-05-07 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_profile_common_user_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='common_user_tags',
            field=models.CharField(default='False', max_length=200),
        ),
    ]