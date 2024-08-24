from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from bot_core import settings, views
from admin_panel.views import index

urlpatterns = [
    path('bot/', include("admin_panel.urls")),
    path('', index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

