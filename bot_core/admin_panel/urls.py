from django.urls import path
from . import views
from .views import access_required

urlpatterns = [
    path('users/', access_required(4)(views.users), name='users'),
    path('users/<int:user_id>/', access_required(4)(views.user), name='user'),
    path('start-bot/', access_required(4)(views.start_bot_view), name='start-bot'),
    path('stop-bot/', access_required(4)(views.stop_bot_view), name='stop-bot'),
    path('restart-bot/', access_required(4)(views.restart_bot_view), name='restart-bot'),
    path('status/', access_required(3)(views.bot_status_view), name='bot-status'),
    path('settings/', access_required(3)(views.bot_settings), name='bot_settings'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),

    path('bot_settings/', access_required(3)(views.bot_settings), name='bot_settings'),
    path('create_topic/', access_required(3)(views.create_topic), name='create_topic'),
    path('edit_topic/<int:topic_id>/', access_required(3)(views.edit_topic), name='edit_topic'),
    path('delete_topic/<int:topic_id>/', access_required(3)(views.delete_topic), name='delete_topic'),
    path('add_question/<int:topic_id>/', access_required(3)(views.add_question), name='add_question'),
    path('edit_question/<int:question_id>/', access_required(3)(views.edit_question), name='edit_question'),
    path('delete_question/<int:question_id>/', access_required(3)(views.delete_question), name='delete_question'),
]
