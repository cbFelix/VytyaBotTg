from django.urls import path
from . import views

urlpatterns = [
    path('bot_menu/', views.bot_menu, name='bot_menu'),
    path('bot_configure/', views.bot_configure, name='bot-configure'),
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.user, name='user'),
    path('start-bot/', views.start_bot_view, name='start-bot'),
    path('stop-bot/', views.stop_bot_view, name='stop-bot'),
    path('restart-bot/', views.restart_bot_view, name='restart-bot'),
    path('status/', views.bot_status_view, name='bot-status'),
    path('bot-configure/', views.bot_configure, name='bot_configure'),
]
