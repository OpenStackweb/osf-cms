# Generated by Django 2.0.1 on 2018-02-23 17:50

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_squashed_0086_auto_20180221_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listitem',
            name='caption',
            field=tinymce.models.HTMLField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='listitem',
            name='title',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='type',
            field=models.CharField(choices=[('BLOCK', 'Block'), ('SPONSORSHIP', 'Sponsorship'), ('IMAGEGALLERY', 'Image gallery'), ('VIDEOGALLERY', 'Video gallery'), ('POSTCATEGORY', 'Post category')], max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(),
        ),
    ]
