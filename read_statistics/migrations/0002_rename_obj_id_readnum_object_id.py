# Generated by Django 3.2.4 on 2021-06-17 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='readnum',
            old_name='obj_id',
            new_name='object_id',
        ),
    ]
