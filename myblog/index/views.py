from django.shortcuts import render
from django.http import JsonResponse
import common.config as cf
from user.models import UserProfile


# Create your views here.
def index(request, username=None):
    try:
        if request.method == "GET":

            if username:
                try:
                    auser = UserProfile.objects.get(username = username)
                    return render(request, "list.html",locals())
                except:
                    result = {"code": 401, "error": cf.resmsg["401"]}
                    return JsonResponse(result)
            else:
                return render(request, "index.html")
        elif request.method == "POST":
            result = {"code": 200, "error": ""}
            return JsonResponse(result)
        else:
            result = {"code": 470, "error": cf.resmsg["470"]}
            return JsonResponse(result)
    except Exception as e:
        result = {"code": 499, "error": cf.resmsg["499"]}
        # result = {"code": 499, "error": e}
        return JsonResponse(result)
