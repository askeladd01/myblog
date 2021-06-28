from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount, LikeRecord


# Create your views here.
def SuccessResponse(like_record, liked_num):
    data = {'status': 'SUCCESS', 'like_record': like_record, 'liked_num': liked_num}
    return JsonResponse(data)


def like_change(request):
    user = request.user
    if not user.is_authenticated:
        data = {'code': 400, 'message': '请先登录'}
        return JsonResponse(data)

    content_type = request.GET.get('content_type')
    content_type = ContentType.objects.get(model=content_type)
    object_id = request.GET.get('object_id')

    # 先判断用户是否有点赞记录
    like_record, is_created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
    # 用户新建点赞，总点赞数加一
    if is_created:
        like_count, is_created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
        like_count.like_num += 1
        like_count.save()
        like_record = True

        return SuccessResponse(like_record, like_count.like_num)
    else:
        # 删除用户点赞记录
        like_record.delete()
        like_record = False
        # 总点赞数减一
        like_count = LikeCount.objects.get(content_type=content_type, object_id=object_id)
        like_count.like_num -= 1
        like_count.save()
        return SuccessResponse(like_record, like_count.like_num)
