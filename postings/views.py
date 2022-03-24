import json

from django.http  import JsonResponse
from django.views import View
from django.forms import ValidationError

from postings.models import Post, Image
from users.util      import login_decorator

class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            text = data['text']
            image_list = data['image'].split(',')
            
            
            
            
            
            post = Post.objects.create(
                user = user,
                text = text
            )
            
            for image in image_list:
                Image.objects.create(
                    image_url = image,
                    post = post
                )
            return JsonResponse({'Message' : 'Success'}, status=201)
        except KeyError:
            return JsonResponse({'Message' : 'Key_Error'}, status=400)
        except ValidationError as e:
            return JsonResponse({'Message' : 'Image Does Not Exist'}, status=400)