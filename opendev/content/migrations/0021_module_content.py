# Generated by Django 2.0.1 on 2018-01-12 16:23

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_auto_20180112_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='content',
            field=tinymce.models.HTMLField(blank=True, max_length=65535),
        ),
    ]
