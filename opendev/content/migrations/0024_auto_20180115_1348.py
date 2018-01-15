# Generated by Django 2.0.1 on 2018-01-15 13:48

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_auto_20180112_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listitem',
            name='icon',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='image',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=200, null=True),
        ),
    ]
