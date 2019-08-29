from django.http import JsonResponse
from common import my_jwt, config
from user import models


def login_check(*methods):
    def _login_check(func):
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return func(request, *args, **kwargs)

            # 校验 token
            # 校验不通过,return JsonResponse()
            token = request.META.get("HTTP_AUTHORIZATION")
            if not token:
                result = {"code": 107, "error": "token不能为空"}
                return JsonResponse(result)

            try:
                payload = my_jwt.Jwt.decode(token, config.key)
            except:
                result = {"code": 108, "error": "请登录"}
                return JsonResponse(result)

            # 查询user
            username = payload["username"]
            try:
                user = models.User.objects.get(username=username)
                request.user = user
            except:
                result = {"code": 109, "error": "用户不存在"}
                return JsonResponse(result)

            return func(request, *args, **kwargs)

        return wrapper

    return _login_check
