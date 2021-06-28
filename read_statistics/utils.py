import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from blog.models import Blog


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    cookies_key = f'{ct.model}_{obj.pk}_read'
    if not request.COOKIES.get(cookies_key):

        read_obj, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        read_obj.read_num += 1
        read_obj.save()

        date = timezone.now().date()
        read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        read_detail.read_num += 1
        read_detail.save()
    return cookies_key


def get_week_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_data = ReadDetail.objects.filter(content_type=content_type, date=date)
        res = read_data.aggregate(read_date_sum=Sum('read_num'))
        read_nums.append(res['read_date_sum'] or 0)
    return dates, read_nums


def get_today_hot_blog():
    today = timezone.now().date()
    hot_blog = Blog.objects.filter(read_details__date=today).values('id', 'title')\
        .annotate(hot_blogs_num=Sum('read_details__read_num')).order_by('-hot_blogs_num')
    return hot_blog[:7]


def get_yesterday_hot_blog():
    yesterday = timezone.now().date()-datetime.timedelta(days=1)
    hot_blog = Blog.objects.filter(read_details__date=yesterday).values('id', 'title')\
        .annotate(hot_blogs_num=Sum('read_details__read_num')).order_by('-hot_blogs_num')
    return hot_blog[:7]


def get_week_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    hot_blog = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date).values('id', 'title')\
        .annotate(hot_blogs_num=Sum('read_details__read_num')).order_by('-hot_blogs_num')
    return hot_blog[:7]
