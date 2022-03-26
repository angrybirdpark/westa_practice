from email import contentmanager
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
            comments = post.comment_set.all()
            results_comments = []
            
            for comment in comments:
                results_comments.append(
                    {
                        'id'      : comment.id,
                        'userName': comment.user.id,
                        'content' : comment.comment,
                        'isliked' : True
                    }
                )

            results.append(
                {
                    'postId'     : post.id,
                    'profileName': User.objects.get(id = post.user.id).name,
                    'profileUrl' : "https://hhspress.org/wp-content/uploads/2020/05/2-24435_red-angry-birds-red-angry-birds-png-transparent.png",
                    'contentUrl' : [image.image_url for image in post.image_set.all()],
                    'feedContent': post.content,
                    'commentList': results_comments
                }
            )
        return JsonResponse({'Posting' : results}, status=201)

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
                    'content_id'   : comment.id,
                    'content'      : comment.comment,
                    'name'         : User.objects.get(id = comment.user.id).name,
                    'post_id'      : Post.objects.get(id = comment.post.id).id,
                    'post'         : Post.objects.get(id = comment.post.id).content
                }
            )
        return JsonResponse({'Comment' : results}, status=201)