from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import common.config as cf
from common import mytoken
from .models import UserProfile
import json
from common.check import check_token


# Create your views here.
def register(request):
    try:
        if request.method == "GET":
            return render(request, "register.html")
        elif request.method == "POST":
            json_str = request.body
            json_obj = json.loads(json_str)
            username = json_obj.get("username")
            password1 = json_obj.get("password1")
            password2 = json_obj.get("password2")
            email = json_obj.get("email")
            nickname = json_obj.get("nickname", username)
            sign = json_obj.get("sign", '世界那么大,我想去看看')

            if not username:
                result = {"code": 301, "error": cf.resmsg["301"]}
                return JsonResponse(result)

            if not password1 or not password2:
                result = {"code": 302, "error": cf.resmsg["302"]}
                return JsonResponse(result)

            if password1 != password2:
                result = {"code": 303, "error": cf.resmsg["303"]}
                return JsonResponse(result)

            if not email:
                result = {"code": 304, "error": cf.resmsg["304"]}
                return JsonResponse(result)

            user = UserProfile.objects.filter(username=username)
            if user:
                result = {"code": 305, "error": cf.resmsg["305"]}
                return JsonResponse(result)

            password = mytoken.pwd(password1)

            UserProfile.objects.create(
                username=username,
                password=password,
                nickname=nickname,
                email=email,
                sign=sign
            )

            token = mytoken.token(username)
            result = {"code": 200, "error": "", "username": username, "data": {"token": token}}
            return JsonResponse(result)
        else:
            result = {"code": 370, "error": cf.resmsg["370"]}
            return JsonResponse(result)
    except Exception as e:
        result = {"code": 399, "error": e}
        # result = {"code": 399, "error": cf.resmsg["399"]}
        return JsonResponse(result)


def login(request):
    try:
        if request.method == "GET":
            return render(request, "login.html")
        elif request.method == "POST":
            json_obj = json.loads(request.body)
            username = json_obj.get("username")
            password = json_obj.get("password")
            if not username or not password:
                # "311": "用户名和密码不能为空",
                result = {"code": 311, "error": cf.resmsg["311"]}
                return JsonResponse(result)
            try:
                auser = UserProfile.objects.get(username=username)
                pwd = mytoken.pwd(password)
                if pwd == auser.password:
                    token = mytoken.token(username)
                    result = {"code": 200, "error": "", "username": username, "data": {"token": token}}
                    return JsonResponse(result)
                else:
                    # "312": "用户名或密码错误",
                    result = {"code": 312, "error": cf.resmsg["312"]}
                    return JsonResponse(result)
            except:
                # "312": "用户名或密码错误",
                result = {"code": 312, "error": cf.resmsg["312"]}
                return JsonResponse(result)
        else:
            result = {"code": 371, "error": cf.resmsg["371"]}
            return JsonResponse(result)
    except:
        result = {"code": 398, "error": cf.resmsg["398"]}
        return JsonResponse(result)


@check_token("GET","PUT")
def change_info(request, username):
    try:
        if request.method == "GET":
            if not username:
                result = cf.error_msg("394")
                return JsonResponse(result)
            user = request.user
            if user.username != username:
                result = cf.error_msg("393")
                return JsonResponse(result)
            data = {
                "avatar": "" if not user.avatar else str(user.avatar),
                "nickname": user.nickname,
                "sign": user.sign,
                "info": user.info
            }
            result = {"code": 200, "error": "", "data": data}
            return JsonResponse(result)
        elif request.method == "PUT":
            user = request.user
            if user.username != username:
                result = cf.error_msg("395")
                return JsonResponse(result)
            json_str = request.body
            if not json_str:
                result = cf.error_msg("322")
                return JsonResponse(result)

            userinfo = json.loads(json_str)
            if not userinfo.get("nickname"):
                result = cf.error_msg("323")
                return JsonResponse(result)

            request.user.nickname = userinfo.get("nickname")
            request.user.sign = userinfo.get("sign")
            request.user.info = userinfo.get("info")
            request.user.save()
            result = {"code": 200, "error": ""}
            return JsonResponse(result)
        else:
            result = cf.error_msg("395")
            return JsonResponse(result)
    except Exception as e:
        result = cf.error_msg("397")
        return JsonResponse(result)


def change(request, username):
    return render(request, "change_info.html")

@check_token("POST")
def avatar(request,username):
    try:
        if request.method != "POST":
            result = cf.error_msg("391")
            return JsonResponse(result)
        user = request.user
        if user.username != username:
            result = cf.error_msg("392")
            return JsonResponse(result)

        avatar = request.FILES.get("avatar")
        if not avatar:
            result = cf.error_msg("321")
            return JsonResponse(result)
        print(avatar)
        request.user.avatar = avatar
        request.user.save()
        result = {"code": 200, "error": ""}
        return JsonResponse(result)
    except Exception as e:
        result = cf.error_msg("390",msg=e)
        return JsonResponse(result)
