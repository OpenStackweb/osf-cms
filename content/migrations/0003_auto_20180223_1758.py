# Generated by Django 2.0.1 on 2018-02-23 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20180223_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listitem',
            name='caption',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
