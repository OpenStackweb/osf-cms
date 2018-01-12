# Generated by Django 2.0.1 on 2018-01-11 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_auto_20180111_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='background_color',
            field=models.CharField(choices=[('BLACK', 'Black'), ('WHITE', 'White'), ('DARKGREY', 'Dark grey'), ('LIGHTGREY', 'Light grey'), ('RED', 'Red'), ('LIGHTBLUE', 'Light blue')], default='BLACK', max_length=9),
        ),
        migrations.AddField(
            model_name='module',
            name='font_color',
            field=models.CharField(choices=[('BLACK', 'Black'), ('WHITE', 'White')], default='WHITE', max_length=9),
        ),
        migrations.AlterField(
            model_name='module',
            name='page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modules', to='content.Page'),
        ),
    ]
