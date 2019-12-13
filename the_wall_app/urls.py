from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('register', views.register),
    path('check_login', views.check_login),
    path('wall', views.wall),
    path('create_message', views.create_message),
    path('post_comment', views.post_comment),
    path('delete_message/<int:message_id>', views.delete_message),
    path('logout', views.logout),
]