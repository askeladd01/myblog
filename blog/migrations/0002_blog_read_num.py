# Generated by Django 3.2.4 on 2021-06-16 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='read_num',
            field=models.IntegerField(default=0, verbose_name='阅读量'),
        ),
    ]
