# Generated by Django 2.0.1 on 2018-01-22 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0051_auto_20180122_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
