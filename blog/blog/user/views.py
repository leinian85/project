from django.http import JsonResponse
import json
from . import models
import hashlib
from common import my_jwt
from common import config


# Create your views here.
def users(request, username=None):
    result = {"code": 200, "error": ""}

    if request.method == "GET":
        if username:
            print("username:",username)
            try:
                user = models.User.objects.get(username=username)
                print("user.info:",user.username)
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

    elif request.method == "PUT":
        # 更新数据
        pass
    else:
        result["code"] = 110
        result["error"] = "无效的请求"

    return JsonResponse(result)
