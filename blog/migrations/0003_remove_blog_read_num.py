# Generated by Django 3.2.4 on 2021-06-17 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_read_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='read_num',
        ),
    ]