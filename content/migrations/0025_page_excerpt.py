# Generated by Django 2.0.1 on 2018-03-15 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0024_auto_20180315_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='excerpt',
            field=models.TextField(default='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean tortor metus, pretium et diam sed, feugiat feugiat ligula. Morbi id urna neque. Vivamus egestas mauris a egestas varius. Donec vestibulum nisi odio, non malesuada nisl pellentesque non. Mauris at interdum purus, faucibus molestie justo. Sed id pharetra enim.', max_length=350),
            preserve_default=False,
        ),
    ]
