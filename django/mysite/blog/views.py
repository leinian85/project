from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models

def index(request):
    return render(request,"blog/index.html")

def list(request):
    return render(request, "blog/list.html")

def mypic(request):
    return render(request, "blog/mypic.html")

def login(request):
    if request.method == "GET":
        username = request.COOKIES.get("username","")
        return render(request, "blog/login.html",locals())
    elif request.method == "POST":
        username = request.POST.get("username")
        if username == "":
            user_error = "用户名不能为空"
            return render(request, "blog/login.html", locals())

        password = request.POST.get("password")
        if password == "":
            password_error = "密码不能为空"
            return render(request, "blog/login.html", locals())

        try:
            user = models.User.objects.get(name = username,password = password)
            request.session["user"] = {
                "username" : user.name,
                "id": user.id,
            }

            # reps = render(request, "blog/index.html", locals())
            # if "remember" in request.POST:
            #     reps.set_cookie("username",username)
            #
            # return reps
            reps = HttpResponseRedirect("/blog/index")
            reps.set_cookie("username",username)
            return reps

        except:
            password_error = "用户名或密码不正确"
            return render(request, "blog/login.html", locals())

def regist(request):
    if request.method == "GET":
        return render(request, "blog/regist.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if len(username)<6:
            user_error = "用户名太短"
            return render(request, "blog/regist.html", locals())
        if len(password1) == 0:
            password1_error = "密码不能为空"
            return render(request, "blog/regist.html", locals())
        if len(password2) == 0:
            password2_error = "密码不能为空"
            return render(request, "blog/regist.html", locals())
        if password1 != password2:
            password2_error = "两次密码不一致"
            password1 = password2 = ""
            return render(request, "blog/regist.html", locals())
        try:
            user = models.User.objects.get(name = username)
            user_error = "用户已存在"
            return render(request, "blog/regist.html", locals())
        except Exception as e:
            user = models.User.objects.create(
                name=username,
                password = password1
            )
            msg = "注册成功!"
            request.session["user"] = {"username":username}
            return render(request, "blog/ok.html", locals())

def logout(request):
    if "user" in request.session:
        del request.session["user"]
        return render(request, "blog/index.html", locals())


