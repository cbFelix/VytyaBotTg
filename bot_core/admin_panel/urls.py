# urls.py

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
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/edit/', views.topic_edit, name='topic_edit'),
    path('topics/<int:topic_id>/questions/', views.question_list, name='question_list'),
    path('topics/<int:topic_id>/questions/edit/', views.question_edit, name='question_edit'),
    path('topics/<int:topic_id>/questions/edit/<int:question_id>/', views.question_edit, name='question_edit'),
]
