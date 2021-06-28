from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader import fields
from django.urls import reverse

from read_statistics.models import ReadDetail


# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(max_length=15, verbose_name='博文分类')

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='博客标题')
    content = fields.RichTextUploadingField(verbose_name='博客内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    last_edit_time = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    read_details = GenericRelation(ReadDetail)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name='博文分类')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='博文作者')

    def __str__(self):
        return f'博客标题:{self.title}'

    class Meta:
        ordering = ['-created_time']

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})