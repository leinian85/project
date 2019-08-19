from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=40, verbose_name="姓名")
    sex = models.IntegerField(null=True, verbose_name="性别")
    age = models.IntegerField(null=True, verbose_name="年龄")

    def __str__(self):
        return self.name

class Pub(models.Model):
    name = models.CharField(max_length=100, verbose_name="出版社名称")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="书名")
    author = models.ForeignKey(Author, null=True, verbose_name="作者")  # 外键
    pub = models.ForeignKey(Pub, null=True, verbose_name="出版社")  # 外键

    def __str__(self):
        return self.title
