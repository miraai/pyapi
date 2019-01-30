# urls.py
from django.conf.urls import url
from api import views

urlpatterns = [
    # url('', views.index, name='index'),
    url('register/', views.register_user, name='register'),
    url('login/', views.login_user, name='login'),
    url('post/', views.post_content, name='post_content'),
    url('like/', views.like_post, name='like_post')
]
