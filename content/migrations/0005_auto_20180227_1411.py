# Generated by Django 2.0.1 on 2018-02-27 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20180227_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
