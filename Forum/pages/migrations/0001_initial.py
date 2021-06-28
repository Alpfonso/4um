# Generated by Django 3.2 on 2021-05-02 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('profile_description', models.TextField(default='Enter short profile description', max_length=255)),
            ],
        ),
    ]
