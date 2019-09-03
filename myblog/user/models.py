from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True,verbose_name="用户id")
    username = models.CharField(max_length=30,unique=True,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")
    nickname = models.CharField(max_length=30,verbose_name="昵称")
    tel = models.CharField(max_length=11,verbose_name="手机号",null=True)
    email = models.CharField(max_length=50,verbose_name="邮箱")
    sign = models.CharField(max_length=50,verbose_name="个人签名",null=True)
    info = models.CharField(max_length=150,verbose_name="个人描述",null=True)
    avatar = models.ImageField(upload_to='static/avatar/',null=True)

    class Meta:
        db_table = "user"