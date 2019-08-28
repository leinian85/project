from django.shortcuts import render
from django.http import JsonResponse
import json
from user.myexcept import DataError
from . import models
import hashlib
from . import my_jwt

# Create your views here.
def users(request):
    key = "leinian"
    redata = {"code":200,"error":""}

    if request.method == "GET":
        # 获取用户数据
        pass
    elif request.method == "POST":
        # 创建用户
        cdata = json.loads(request.body)
        username = cdata["username"]
        email= cdata["email"]
        password_1= cdata["password_1"]
        password_2= cdata["password_2"]
        hs = hashlib.md5()
        hs.update(password_1.encode())
        password = hs.hexdigest()

        if len(password_1) == 0 or len(username) == 0:
            redata["code"] = 201
            redata["error"] = "用户名或密码不能为空"
            return JsonResponse(redata)

        if password_1 != password_2:
            redata["code"] = 202
            redata["error"] = "2次输入的密码不一致"
            return JsonResponse(redata)

        try:
            auser = models.User.objects.get(username = username)
            redata["code"] = 203
            redata["error"] = "用户名已存在"
            return JsonResponse(redata)
        except:
            pass

        try:
            user = models.User()
            user.username = username
            user.password = password
            user.nickname = username
            user.email = email
            user.save()
        except:
            redata["code"] = 203
            redata["error"] = "数据不正确"
            return JsonResponse(redata)

        payload = {"username":username}
        jwt = my_jwt.Jwt()
        token = jwt.encode(payload,key,24*60*60)
        data = {"token":token.decode()}
        redata = {"data":data,"username":username,"code":200}

    elif request.method == "PUT":
        # 更新数据
        pass
    else:
        raise DataError("请求无效")

    return JsonResponse(redata)