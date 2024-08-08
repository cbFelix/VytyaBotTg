from django.shortcuts import render
from admin_panel.bot_manager import load_state


def index(request):
    bot_status = "running" if load_state() else "stopped"
    return render(request, 'base/index.html', {'bot_status': bot_status})
