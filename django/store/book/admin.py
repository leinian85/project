from django.contrib import admin
from . import models

class AuthorManage(admin.ModelAdmin):
    list_display = ["name", "sex", "age"]

class PubManage(admin.ModelAdmin):
    list_display = ["name"]

class BookManage(admin.ModelAdmin):
    # 此处的外键 author,pub 会显示对应的类中的 __str__ 方法返回的值
    list_display = ["title", "author", "pub"]
    list_editable = ["pub"]  # 可编辑字段
    list_filter = ["pub"]   # 过滤

admin.site.register(models.Author, AuthorManage)
admin.site.register(models.Pub, PubManage)
admin.site.register(models.Book, BookManage)
