# Generated by Django 2.0.1 on 2018-01-17 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0040_auto_20180117_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=40)),
                ('url', models.URLField()),
            ],
        ),
    ]
