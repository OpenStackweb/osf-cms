# Generated by Django 2.0.1 on 2018-03-15 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_post_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='posts', to='content.PostCategory'),
        ),
    ]
