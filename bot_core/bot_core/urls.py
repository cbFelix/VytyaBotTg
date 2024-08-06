from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('bot/', include("admin_panel.urls"))
]

