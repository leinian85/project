from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=40,verbose_name="用户名")
    password = models.CharField(max_length=40,verbose_name="密码")
    tel = models.CharField(null=True,max_length=11,verbose_name="手机号")