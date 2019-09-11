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
                    auser = UserProfile.objects.get(username=username)
                    return render(request, "list.html", locals())
                except:
                    result = cf.error_msg("410")
                    return JsonResponse(result)
            else:
                return render(request, "index.html")
        elif request.method == "POST":
            result = {"code": 200, "error": ""}
            return JsonResponse(result)
        else:
            result = cf.error_msg("470")
            return JsonResponse(result)
    except Exception as e:
        result = cf.error_msg("499", msg=e)
        return JsonResponse(result)
