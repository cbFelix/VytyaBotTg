from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from bot_core import settings
from django.db.models import Q
from .bot_manager import stop_bot, load_state, start_bot
from .models import TgUser, UserMessage, Topic, Question
from django.views.decorators.http import require_POST, require_GET

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

def bot_settings(request):
    # Получение всех тем и вопросов для отображения на странице
    topics = Topic.objects.all()

    if request.method == 'POST':
        # Обработка создания или обновления темы
        if 'create_topic' in request.POST:
            topic_name = request.POST.get('topic_name')
            if topic_name:
                Topic.objects.create(name=topic_name)
            return redirect('bot_settings')

        # Обработка создания или обновления вопроса
        if 'create_question' in request.POST:
            topic_id = request.POST.get('topic_id')
            question_text = request.POST.get('question_text')
            answer_text = request.POST.get('answer_text')
            if topic_id and question_text and answer_text:
                topic = get_object_or_404(Topic, id=topic_id)
                Question.objects.create(topic=topic, question_text=question_text, answer_text=answer_text)
            return redirect('bot_settings')

    return render(request, 'bot/bot_settings.html', {'topics': topics})


