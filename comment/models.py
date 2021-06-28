import threading
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from myblog import settings


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    comment_text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, verbose_name='评论用户')

    # 表内数据自关联，回复指向父级评论
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['comment_time']

    def send_email(self):
        if self.parent:
            subject = '有人回复你的评论'
            email = self.reply_to.email
        else:
            subject = '有人评论你的博客'
            email = self.user.email
        context = {'comment_text': self.comment_text, 'url': self.content_object.get_url()}
        text = render_to_string('comment/send_email.html', context)
        send_email = SendEmail(subject, text, email)
        send_email.start()


class SendEmail(threading.Thread):
    def __init__(self, subject, text, email):
        self.subject = subject
        self.text = text
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, '', settings.EMAIL_HOST_USER, [self.email], fail_silently=False, html_message=self.text)
