# Generated by Django 2.0.1 on 2018-03-13 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0019_auto_20180313_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='display_title',
            field=models.BooleanField(default=True),
        ),
    ]
