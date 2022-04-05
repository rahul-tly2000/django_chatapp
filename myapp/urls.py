from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chat-home'),
    path('register/', views.register, name='chat-register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='chat-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='chat-logout'),
    path('home/', views.home, name='chat-home'),
    path('profile/', views.profile, name='chat-profile'),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),
]