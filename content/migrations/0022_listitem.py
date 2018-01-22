# Generated by Django 2.0.1 on 2018-01-12 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0021_module_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='')),
                ('caption', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_items', to='content.Module')),
            ],
            options={
                'verbose_name_plural': 'List items',
                'ordering': ('order',),
            },
        ),
    ]