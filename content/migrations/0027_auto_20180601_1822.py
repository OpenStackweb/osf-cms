# Generated by Django 2.0.1 on 2018-06-01 18:22

from django.db import migrations, models
import tagulous.models.fields
import tagulous.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_auto_20180601_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tagulous_Post_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, help_text='Enter a comma-separated tag string', to='content.Tagulous_Post_tags'),
        ),
        migrations.AlterUniqueTogether(
            name='tagulous_post_tags',
            unique_together={('slug',)},
        ),
    ]
