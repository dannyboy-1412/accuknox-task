from django.urls import path

from .views.user_views import register_user, user_login, search_users
from .views.friend_views import send_friend_request, respond_friend_request, list_friends

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('search/', search_users, name='search'),
    path('send/<int:pk>', send_friend_request, name='send-request'),
    path('respond/<int:pk>/<int:is_accept>', respond_friend_request, name='respond-request'),
    path('friends/', list_friends, name='list-friends'),
]