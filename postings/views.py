import json

from django.http  import JsonResponse
from django.views import View
from django.forms import ValidationError

from postings.models import Post, Image, Comment
from users.util      import login_decorator
from users.validator import image_url_validate
from users.models    import User

class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data             = json.loads(request.body)
            input_user       = request.user
            input_content    = data['content']
            input_image_list = data['image_url'].split(',')
            
            for image in input_image_list:
                image_url_validate(image)
            
            if len(input_image_list) > 10 :
                return JsonResponse({'Message' : 'Images cannot exceed 10'})
            
            post = Post.objects.create(
                user    = input_user,
                content = input_content
            )
            
            for image in input_image_list:
                Image.objects.create(
                    image_url = image,
                    post      = post
                )
            return JsonResponse({'Message' : 'Success'}, status=201)
        
        except KeyError:
            return JsonResponse({'Message' : 'Key_Error'}, status=400)
        except ValidationError as e:
            return JsonResponse({'Message' : 'Image Does Not Exist'}, status=400)

    @login_decorator
    def get(self, request):
        posts = Post.objects.all()
        results = []
        
        for post in posts:
            results.append(
                {
                    'post_id'   : post.id,
                    'user_id'   : User.objects.get(id = post.user.id).id,
                    'name'      : User.objects.get(id = post.user.id).name,
                    'content'   : post.content,
                    'images'    : [image.image_url for image in post.image_set.all()],
                    'created_at': post.created_at
                }
            )
        return JsonResponse({'Post' : results}, status=201)

class CommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            input_user = request.user
            input_post = Post.objects.get(id = data['post_id'])
            input_comment = data['comment']
            
            Comment.objects.create(
                user = input_user,
                post = input_post,
                comment = input_comment
            )
            
            return JsonResponse({'Message' : 'Post created!'}, status=200)

        except KeyError:
            return JsonResponse({'Message' : 'Key_Error'}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'Message' : "Posting Does Not Exist"}, status=400)
        
    @login_decorator
    def get(self, request):
        comments = Comment.objects.all()
        results = []
        
        for comment in comments:
            results.append(
                {
                    'content_id': comment.id,
                    'content'   : comment.comment,
                    'name'      : User.objects.get(id = comment.user.id).name,
                    'post'      : Post.objects.get(id = comment.post.id).content
                }
            )
        return JsonResponse({'Comment' : results}, status=201)