from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from ..models import ReadNum

register = template.Library()


@register.simple_tag
def get_read_num(obj):
    try:
        ct = ContentType.objects.get_for_model(obj)
        read_obj = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        return read_obj.read_num
    except exceptions.ObjectDoesNotExist:
        return 0
