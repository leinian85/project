from django.shortcuts import render
from django.http import JsonResponse
import common.config as cf


# Create your views here.
def index(request, username=None):
    try:
        if request.method == "GET":
            return render(request, "index/index.html")
        elif request.method == "POST":

            result = {"code": 200, "error": ""}
            return JsonResponse(result)
        else:
            result = {"code": 406, "error": cf.resmsg["306"]}
            return JsonResponse(result)
    except Exception as e:
        # result = {"code": 101, "error": cf.resmsg["100"]}
        result = {"code": 101, "error": e}
        return JsonResponse(result)
