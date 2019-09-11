from django.http import JsonResponse
import common.config as cf
from common import mytoken
from user.models import UserProfile

def check_token(*methods):
    def _check_token(func):
        def wrapper(request,*args,**kwargs):
            if request.method not in methods:
                return func(request,*args,**kwargs)
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                result = cf.error_msg("601")
                return JsonResponse(result)

            try:
                username =mytoken.username_for_token(token)
                auser = UserProfile.objects.get(username = username)
                request.user = auser
            except Exception as e:
                result = cf.error_msg("602",msg=e)
                return JsonResponse(result)

            return func(request,*args,**kwargs)
        return wrapper
    return _check_token