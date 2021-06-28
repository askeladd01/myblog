from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from blog import models
from read_statistics.utils import read_statistics_once_read


# Create your views here.


class Pagination(object):
    def __init__(self, current_page, all_count, per_page_num=2, pager_count=11):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        page_html_list.append('''
                    <nav aria-label='Page navigation>'
                    <ul class='pagination'>
                ''')
        first_page = '<li><a href="?page=%s">首页</a></li>' % (1)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            prev_page = '<li><a href="?page=%s">上一页</a></li>' % (self.current_page - 1,)

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = f'<li class="active"><span>{i}</span></li>'
            else:
                temp = f'<li><a href="?page={i}">{i}</a></li>'
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?page=%s">下一页</a></li>' % (self.current_page + 1,)
        page_html_list.append(next_page)

        last_page = '<li><a href="?page=%s">尾页</a></li>' % (self.all_pager,)
        page_html_list.append(last_page)
        # 尾部添加标签
        page_html_list.append('''
                                           </nav>
                                           </ul>
                                       ''')
        return ''.join(page_html_list)


def get_blog_list_common(request, blogs):
    context = {}
    current_page = request.GET.get('page', 1)
    all_count = blogs.count()
    context['all_count'] = all_count
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=2)
    context['page_obj'] = page_obj
    page_queryset = blogs[page_obj.start:page_obj.end]
    context['page_queryset'] = page_queryset
    context['blog_types'] = models.BlogType.objects.annotate(blog_count=Count('blog'))

    blog_dates = models.Blog.objects.dates('created_time', 'month', order='DESC')
    blog_date_dict = {}
    for blog_date in blog_dates:
        blog_count = models.Blog.objects.filter(created_time__year=blog_date.year,
                                                created_time__month=blog_date.month).count()
        blog_date_dict[blog_date] = blog_count
    context['blog_date_info'] = blog_date_dict
    return context


def blog_list(request):
    blogs = models.Blog.objects.all()
    context = get_blog_list_common(request, blogs)

    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    content = {}
    blog_info = get_object_or_404(models.Blog, pk=blog_pk)
    read_cookies_key = read_statistics_once_read(request, blog_info)

    content['previous_blog'] = models.Blog.objects.filter(pk__lt=blog_pk).first()
    content['next_blog'] = models.Blog.objects.filter(pk__gt=blog_pk).last()
    content['blog_info'] = blog_info

    response = render(request, 'blog/blog_detail.html', content)
    response.set_cookie(read_cookies_key, 'True')
    return response


def blog_type_info(request, blog_type_pk):
    blogs = models.Blog.objects.filter(blog_type_id=blog_type_pk)
    context = get_blog_list_common(request, blogs)

    blog_type = get_object_or_404(models.BlogType, pk=blog_type_pk)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_type_info.html', context)


def blog_date_info(request, year, month):
    blogs = models.Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common(request, blogs)
    context['date_info'] = f'{year}年{month}月'
    return render(request, 'blog/blog_date_info.html', context)
