# Generated by Django 2.0.1 on 2018-01-17 13:28

from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0031_remove_block_display_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('image', filebrowser.fields.FileBrowseField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='listitem',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Icon'),
        ),
    ]