from django.shortcuts import render
from django.http import JsonResponse
import hashlib
import json
from user.models import User
from common.b64 import *
from common import my_jwt
from common import config


# Create your views here.
def tokens(request):
    result = {"code": 200, "error": ""}

    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj.get("username")
        password = json_obj.get("password")
        print(json_obj)
        if not username or not password:
            result["code"] = 211
            result["error"] = "用户名和密码不能为空"
            return JsonResponse(result)

        usera = User.objects.filter(username=username)
        if not usera:
            result["code"] = 212
            result["error"] = "用户名或密码错误"
            return JsonResponse(result)

        passwordb = pwd(password)
        if passwordb != usera[0].password:
            result["code"] = 213
            result["error"] = "密码错误"
            return JsonResponse(result)

        payload = {"username": username}
        token = my_jwt.Jwt().encode(payload, config.key, config.times)
        result["data"] = {"token": token.decode()}
        result["username"] = username
        print(result)
    else:
        result["code"] = 110
        result["error"] = "无效的请求"

    return JsonResponse(result)
