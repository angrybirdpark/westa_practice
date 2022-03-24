from django.urls import path
from postings.views import PostView

urlpatterns = [
    path('/post', PostView.as_view()),
]