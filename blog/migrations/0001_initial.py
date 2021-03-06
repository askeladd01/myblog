# Generated by Django 3.2.4 on 2021-06-16 14:46

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=15, verbose_name='博文分类')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='博客标题')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='博客内容')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('last_edit_time', models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='博文作者')),
                ('blog_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogtype', verbose_name='博文分类')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]
