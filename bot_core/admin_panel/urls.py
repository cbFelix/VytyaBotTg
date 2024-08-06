from django.urls import path, include
import admin_panel.views as views

urlpatterns = [
    path("", views.index),
    path("users/", views.users),
    path("bot_menu/", views.bot_menu),
    path("cli/", views.cli_menu),

]




