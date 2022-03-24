import jwt

from django.http import JsonResponse
from django.conf import settings

from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs) :
        try:
            access_token = request.header.get('Authorization')
            payload      = jwt.decode(
                                access_token,
                                settings.SECRET_KEY,
                                algorithms=settings.ALGORITHM
                            )
            user         = User.objects.get(id = payload['id'])
            request.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'Message' : 'Invalid_Token'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'Message' : 'Invalid_User'}, status=400)
        return func(self, request, *args, **kwargs)
    
    return wrapper