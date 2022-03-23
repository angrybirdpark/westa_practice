import json, bcrypt, jwt
from django.forms import ValidationError

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models       import User
from users.validator    import email_validate, password_validate

class SignUpView(View):
    def post(self, request):
        try: 
            data               = json.loads(request.body)
            input_name         = data['name']
            input_email        = data['email']
            input_password     = data['password']
            input_phone_number = data['phone_number']
            
            email_validate(input_email)
            password_validate(input_password)
            
            if User.objects.filter(email = input_email).exists():
                return JsonResponse({'Message' : 'Email already exists'}, status=401)

            hashed_password = bcrypt.hashpw(input_password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name         = input_name,
                email        = input_email,
                password     = hashed_password,
                phone_number = input_phone_number,
            )
            return JsonResponse({'Message' : 'Success'}, status=201)
        except KeyError:
            return JsonResponse({'Message' : 'Key_Error'}, status=400)
        except ValidationError as e:
            return JsonResponse({'Message' : 'Invalid_Key'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            input_email    = data['email']
            input_password = data['password']
            user           = User.objects.get(email = input_email)
            
            if not bcrypt.checkpw(input_password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'Message': 'Invalid_User'}, status=401)
            
            access_token = jwt.encode({'id':user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return JsonResponse({'Token' : access_token}, status=200)
            
        except User.DoesNotExist:
            return JsonResponse({'Message': 'Invalid_User'}, status=401)
        
        except KeyError:
            return JsonResponse({'Message' : 'Key_Error'}, status=400)