from django.contrib import admin
from django.urls import path, include
from .views import HomeView, PostView, CommentView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/', PostView.as_view(), name='post'),
    path('comment/', CommentView.as_view(), name='comment'),
]
