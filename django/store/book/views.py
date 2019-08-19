from django.shortcuts import render
from . import models

def index(request):
    if request.method == "GET":
        return render(request,"book/index.html")

def add_book(request):
    pubs = models.Pub.objects.all()
    authors = models.Author.objects.all()
    if request.method == "GET":
        try:
            book = models.Book.objects.get(id = request.GET.get("id"))
        except:
            book = None
    elif request.method =="POST":
        try:
            title = request.POST.get("title")
            pub_id = request.POST.get("pub_id")
            author_id = request.POST.get("author_id")
            models.Book.objects.create(title = title,
                                       pub_id = pub_id,
                                       author_id = author_id)
            msg = "添加成功!"
        except Exception as e:
            msg = e
    return render(request, "book/add.html", locals())


def sel_book(request):
    books = models.Book.objects.all()
    return render(request,"book/sel_book.html",locals())

def update_book(request):
    if request.method == "POST":
        try:
            book = models.Book.objects.get(id = request.POST.get("id"))
            book.title = request.POST.get("title")
            book.author_id = request.POST.get("author_id")
            book.pub_id = request.POST.get("pub_id")
            book.save()
            msg = "修改成功"
            book = None
            pubs = models.Pub.objects.all()
            authors = models.Author.objects.all()
        except Exception as e:
            msg = e
    return render(request,"book/add.html",locals())


def del_book(request):
    if request.method == "GET":
        id = request.GET.get("id")
        book = models.Book.objects.get(id = id)
        book.delete()
    books = models.Book.objects.all()
    return render(request,"book/sel_book.html",locals())