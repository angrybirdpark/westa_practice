import json

from django.http  import JsonResponse
from django.views import View

from postings.models       import Post, Image

class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = ''
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
        except:
            None