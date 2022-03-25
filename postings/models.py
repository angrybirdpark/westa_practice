from django.db import models

# Create your models here.
class Post(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content    = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        
class Image(models.Model):
    image_url = models.CharField(max_length=2000)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'images'
        
class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comments'
