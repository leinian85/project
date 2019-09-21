from django.shortcuts import render
from django.http import JsonResponse
import common.config as cf
import json
import common.mytoken as mytoken
from user.models import UserProfile
from common.check import check_token
from .models import Topic


def gettopic(login_username, username):
    try:
        user = UserProfile.objects.filter(username=username)

        if not user:
            return None
        userl = UserProfile.objects.filter(username = login_username)

        if not userl:
            return None
        # 博主自己访问自己的文章
        auser = user[0]
        if login_username == username:
            topics = auser.topic_set.all()
        else:
            topics = auser.topic_set.filter(limit="public")

        restopics = []
        if not topics:
            return (auser.nickname, restopics)

        for topic in topics:
            t = {}
            t['id'] =  topic.id
            t['title'] =  topic.title
            t['category'] =  topic.category
            t['limit'] =  topic.limit
            t['introduce'] =  topic.introduce
            t['content'] =  topic.content
            t['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
            t['author'] =  auser.nickname
            restopics.append(t)
        return (auser.nickname, restopics)
    except:
        return None


# Create your views here.
@check_token("POST","DELETE")
def topic(request, username):
    try:
        if request.method == "GET":
            try:
                token = request.META.get("HTTP_AUTHORIZATION")
                login_username = mytoken.username_for_token(token)

                datas = gettopic(login_username, username)
                if datas:
                    nickname, topics = datas
                    print('nickname:',nickname)
                    print('topics:',topics)
                else:
                    result = cf.error_msg("518")
                    return JsonResponse(result)

                result = {"code": 200, "error": "", "nickname": nickname, "data": {"topics": topics}}
                return JsonResponse(result)
            except Exception as e:
                result = cf.error_msg("519", msg=e)
                return JsonResponse(result)
        elif request.method == "POST":
            if request.user:
                json_str = request.body
                json_obj = json.loads(json_str)
                content = json_obj["content"]
                content_text = json_obj["content_text"]
                limit = json_obj["limit"]
                title = json_obj["title"]
                category = json_obj["category"]

                topica = Topic()
                topica.title = title
                topica.category = category
                topica.limit = limit
                topica.introduce = content_text[:30]
                topica.content = content
                topica.author_id = request.user.username
                topica.save()
                result = {"code": 200, "error": ""}
                return JsonResponse(result)
            else:
                result = cf.error_msg("517")
                return JsonResponse(result)
        elif request.method == "DELETE":
            if request.user:
                topic_id = request.GET.get("topic_id")
                topic = Topic.objects.filter(id = topic_id,author_id = request.user.username)
                if topic:
                    topic.delete()
                    result = {"code": 200, "error": ""}
                    return JsonResponse(result)
                else:
                    result = cf.error_msg("515")
                    return JsonResponse(result)
            else:
                result = cf.error_msg("516")
                return JsonResponse(result)
        else:
            result = cf.error_msg("570")
            return JsonResponse(result)
    except Exception as e:
        result = cf.error_msg("599", msg=e)
        return JsonResponse(result)


def re_release(request,username):
    if request.method == "GET":
        return render(request, "release.html")


def po_release(request,username):
    try:
        if request.method == "GET":
            token = request.META.get("HTTP_AUTHORIZATION")
            result = cf.error_msg("200")
            return JsonResponse(result)
        elif request.method == "POST":
            result = cf.error_msg("200")
            return JsonResponse(result)
        else:
            result = cf.error_msg("570")
            return JsonResponse(result)
    except Exception as e:
        result = cf.error_msg("598", msg=e)
        return JsonResponse(result)