# Generated by Django 2.0.1 on 2018-01-11 18:24

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20180111_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='page',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
