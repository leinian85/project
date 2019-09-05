from django.shortcuts import render
from django.http import JsonResponse
import common.config as cf
import json
import common.mytoken as mytoken
from user.models import UserProfile


def gettopic(login_username, username):
    try:
        user = UserProfile.objects.filter(username = username)
        print(user)
        if not user:
            return None
        # 博主自己访问自己的文章
        auser = user[0]
        print(auser)
        if login_username == username:
            topics = auser.topic_set.all()
        else:
            topics = auser.topic_set.filter(limit = "public")

        if not topics:
            topics = ""
        return (auser.nickname,topics)
    except:
        return None

# Create your views here.
def topic(request, username):
    try:
        if request.method == "GET":
            try:
                token = request.META.get("HTTP_AUTHORIZATION")

                login_username = mytoken.username_for_token(token)

                datas = gettopic(login_username, username)
                if datas:
                    nickname,topics = datas
                else:
                    result = {"code": 518, "error": cf.resmsg["518"]}
                    return JsonResponse(result)

                result = {"code": 200, "error": "", "nickname":nickname,"data": {"topics":topics}}
                return JsonResponse(result)
            except Exception as e:
                result = {"code": 519, "error": e}
                return JsonResponse(result)
        else:
            result = {"code": 570, "error": cf.resmsg["570"]}
            return JsonResponse(result)
    except Exception as e:
        print(e)
        result = {"code": 599, "error": e}
        # result = {"code": 599, "error": cf.resmsg["599"]}
        return JsonResponse(result)
