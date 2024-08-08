from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.management import call_command
from django.conf import settings
from admin_panel.models import TgUser, UserMessage
from .bot_manager import start_bot, stop_bot, load_state




def bot_menu(request):
    bot_status = "running" if load_state() else "stopped"
    return render(request, 'bot/bot_menu.html', {'bot_status': bot_status})


def users(request):
    query = request.GET.get('q', '')
    users = TgUser.objects.filter(
        Q(user_id__icontains=query) |
        Q(username__icontains=query) |
        Q(phone__icontains=query)
    )
    return render(request, 'bot/users.html', {'users': users})


def user(request, user_id):
    user = TgUser.objects.get(pk=user_id)
    messages = UserMessage.objects.filter(user=user)
    return render(request, 'bot/user.html', {'user': user, 'messages': messages})


@require_POST
def bot_configure(request):
    new_token = request.POST.get('token')
    if new_token:
        settings.TELEGRAM_API_TOKEN = new_token
    return redirect('bot_menu')


@require_GET
def start_bot_view(request):
    try:
        pid = start_bot()
        return JsonResponse({'status': 'running', 'pid': pid})
    except RuntimeError as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_GET
def stop_bot_view(request):
    try:
        stop_bot()
        return JsonResponse({'status': 'stopped'})
    except RuntimeError as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_GET
def restart_bot_view(request):
    try:
        stop_bot()
        pid = start_bot()
        return JsonResponse({'status': 'running', 'pid': pid})
    except RuntimeError as e:
        return JsonResponse({'error': str(e)}, status=400)


def bot_status_view(request):
    bot_status = "running" if load_state() else "stopped"
    return JsonResponse({'status': bot_status})

