from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from blog.models import Blog
from read_statistics import utils


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = utils.get_week_read_data(blog_content_type)

    week_hot_blogs = cache.get('week_hot_blogs')
    if not week_hot_blogs:
        week_hot_blogs = utils.get_week_hot_blog()
        cache.set('week_hot_blog', week_hot_blogs, 3600)

    context = {
        'dates': dates,
        'read_nums': read_nums,
        'today_hot_blogs': utils.get_today_hot_blog(),
        'yesterday_hot_blogs': utils.get_yesterday_hot_blog(),
        'week_hot_blogs': week_hot_blogs
    }
    return render(request, 'home.html', context)
