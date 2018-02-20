# Generated by Django 2.0.1 on 2018-02-20 15:38

from django.db import migrations, models
import filebrowser.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0081_imagegallery_images_per_row'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now_add=True)),
                ('image', filebrowser.fields.FileBrowseField(blank=True, max_length=200, null=True)),
                ('content', tinymce.models.HTMLField(max_length=65535)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
