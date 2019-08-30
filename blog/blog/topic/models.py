from django.db import models
from user.models import User

# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length=50,verbose_name="文章主题")
    # 文章的分类 : 1.tec技术类型 2.no-tec非技术类
    category = models.CharField(max_length=20,verbose_name="文章的分类")
    # 文章权限: 1.public 公开 2.private 私有
    limit = models.CharField(max_length=10,verbose_name="文章权限")
    # 文章简介: 文章内容的前三十个字符
    introduce = models.CharField(max_length=90,verbose_name="文章简介")
    content = models.TextField(verbose_name="博客内容")
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")
    author = models.ForeignKey(User)

    class Meta:
        db_table = "Topic"