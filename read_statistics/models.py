import datetime

from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0, verbose_name='阅读量')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now, verbose_name='阅读日期')
    read_num = models.IntegerField(default=0, verbose_name='阅读量')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')