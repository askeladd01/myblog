from django.http import JsonResponse

from .models import Comment
from .myforms import CommentForm


# Create your views here.

def update_comment(request):
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment_obj = Comment()
        comment_obj.user = comment_form.cleaned_data['user']
        comment_obj.comment_text = comment_form.cleaned_data['comment_text']
        comment_obj.content_object = comment_form.cleaned_data['model_obj']

        parent = comment_form.cleaned_data['parent']
        if parent:
            comment_obj.root = parent.root if parent.root else parent
            comment_obj.parent = parent
            comment_obj.reply_to = parent.user
        comment_obj.save()

        # 邮件通知
        comment_obj.send_email()

        # ajax提交返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment_obj.user.get_nickname_or_username()
        data['comment_time'] = comment_obj.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_text'] = comment_obj.comment_text
        if parent:
            data['reply_to'] = comment_obj.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = None
        data['pk'] = comment_obj.pk
        data['root_pk'] = comment_obj.root.pk if comment_obj.root else None

    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(data)
