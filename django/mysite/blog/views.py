from django.shortcuts import render

def index(request):
    return render(request,"blog/index.html")

def list(request):
    return render(request, "blog/list.html")

def mypic(request):
    return render(request, "blog/mypic.html")

def login(request):
    return render(request, "blog/login.html")

def regist(request):
    return render(request, "blog/regist.html")
