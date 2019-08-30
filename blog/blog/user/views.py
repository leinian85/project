from django.http import JsonResponse
import json
from . import models
import hashlib
from common import my_jwt,config,login_check


# Create your views here.
@login_check.login_check("PUT","GET")
def users(request, username=None):
    result = {"code": 200, "error": ""}

    if request.method == "GET":
        if username:
            try:
                user = models.User.objects.get(username=username)
                data = {}
                if request.GET:
                    for column in request.GET:
                        if hasattr(user,column):
                            data[column] = getattr(user,column)
                else:
                    data = {"info": user.info,
                            "sign": user.sign,
                            "nickname": user.nickname,
                            "avatar": str(user.avatar)}
                result["data"] = data
                result["username"] = username

            except Exception as e:
                result["code"] = 111
                result["error"] = str(e)

            return JsonResponse(result)
        else:
            result["code"] = 110
            result["error"] = "无效的请求"
            return JsonResponse(result)
    elif request.method == "POST":
        # 创建用户
        json_obj = json.loads(request.body)
        username = json_obj.get("username")
        if not username:
            result["code"] = 201
            result["error"] = "用户名不能为空"
            return JsonResponse(result)

        password_1 = json_obj.get("password_1")
        password_2 = json_obj.get("password_2")
        if not password_1 or not password_2:
            result["code"] = 202
            result["error"] = "密码不能为空"
            return JsonResponse(result)

        if password_1 != password_2:
            result["code"] = 203
            result["error"] = "2次输入的密码不一致"
            return JsonResponse(result)

        email = json_obj.get("email")
        if not email:
            result["code"] = 204
            result["error"] = "邮箱不能为空"
            return JsonResponse(result)

        users = models.User.objects.filter(username=username)
        if users:
            result["code"] = 205
            result["error"] = "用户名已存在"
            return JsonResponse(result)

        try:
            hs = hashlib.md5()
            hs.update(password_1.encode())
            password = hs.hexdigest()

            models.User.objects.create(
                username=username,
                password=password,
                nickname=username,
                email=email,
                sign="世界那么大,我来你博客啦"
            )
        except:
            result["code"] = 206
            result["error"] = "数据不正确"
            return JsonResponse(result)

        payload = {"username": username}
        jwt = my_jwt.Jwt()
        token = jwt.encode(payload, config.key, config.times)
        data = {"token": token.decode()}
        result["data"] = data
        result["username"] = username

        return JsonResponse(result)
    elif request.method == "PUT":
        print(request.user)
        if username != request.user.username:
            result["code"] = 207
            result["error"] = "数据异常"
            return JsonResponse(result)

        json_str = request.body
        if not json_str:
            result["code"] = 209
            result["error"] = "数据异常"
            return JsonResponse(result)

        json_obj = json.loads(json_str)
        if 'sign' not in json_obj:
            result["code"] = 210
            result["error"] = "没有 sign"
            return JsonResponse(result)
        if 'info' not in json_obj:
            result["code"] = 211
            result["error"] = "没有 info"
            return JsonResponse(result)
        if 'nickname' not in json_obj:
            result["code"] = 211
            result["error"] = "没有 nickname"
            return JsonResponse(result)

        sign = json_obj["sign"]
        info = json_obj["info"]
        nickname = json_obj["nickname"]
        request.user.sign =sign
        request.user.info =info
        request.user.nickname =nickname
        request.user.save()

        return JsonResponse(result)
    else:
        result["code"] = 110
        result["error"] = "无效的请求"

    return JsonResponse(result)

@login_check.login_check("POST")
def user_avatar(request,username):
    if request.method != "POST":
        result = {"code": 212, "error": "不是post请求"}
        return JsonResponse(result)

    avatat = request.FILES.get("avatar")
    if not avatat:
        result = {"code": 200, "error": "I need avatar"}
        return JsonResponse(result)

    request.user.avatar = avatat
    request.user.save()

    result = {"code":200,"error":"I am avatar"}
    return JsonResponse(result)