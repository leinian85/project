from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import common.config as cf
from common import mytoken
from .models import User
import json,jwt,time


# Create your views here.
def register(request):
    try:
        if request.method == "GET":
            return render(request, "user/register.html")
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


            user = User.objects.filter(username=username)
            if user:
                result = {"code": 305, "error": cf.resmsg["305"]}
                return JsonResponse(result)


            password = mytoken.pwd(password1)

            User.objects.create(
                username=username,
                password=password,
                nickname=nickname,
                email=email,
                sign=sign
            )

            token = mytoken.token(username)
            print(token)
            result = {"code": 200, "error": "","username":username,"data":{"token":token}}
            return JsonResponse(result)
        else:
            result = {"code": 306, "error": cf.resmsg["306"]}
            return JsonResponse(result)
    except Exception as e:
        result = {"code": 100, "error": cf.resmsg["100"]}
        return JsonResponse(result)

def login(request):
    try:
        result = {"code": 200, "error": ""}
        return JsonResponse(result)
    except:
        result = {"code": 100, "error": cf.resmsg["100"]}
        return JsonResponse(result)
