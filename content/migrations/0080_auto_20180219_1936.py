# Generated by Django 2.0.1 on 2018-02-19 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0079_customhtml'),
    ]

    operations = [
        migrations.AddField(
            model_name='customhtml',
            name='kicker',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customhtml',
            name='html_block',
            field=models.TextField(),
        ),
    ]
