from django.db import models

# Create your models here.
class Post(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text       = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        
class Image(models.Model):
    image_url = models.CharField(max_length=2000)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'iamges'