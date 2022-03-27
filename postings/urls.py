from django.urls import path
from postings.views import PostView, CommentView, LikeView

urlpatterns = [
    path('/post', PostView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like', LikeView.as_view()),
]