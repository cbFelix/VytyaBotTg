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

def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'bot/topic_list.html', {'topics': topics})

def topic_edit(request, topic_id=None):
    if topic_id:
        topic = get_object_or_404(Topic, id=topic_id)
    else:
        topic = None

    if request.method == 'POST':
        name = request.POST.get('name')
        if topic:
            topic.name = name
            topic.save()
        else:
            Topic.objects.create(name=name)
        return redirect('topic_list')

    return render(request, 'bot/topic_edit.html', {'topic': topic})

def question_list(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    questions = topic.questions.all()
    return render(request, 'bot/question_list.html', {'topic': topic, 'questions': questions})

def question_edit(request, topic_id, question_id=None):
    topic = get_object_or_404(Topic, id=topic_id)
    if question_id:
        question = get_object_or_404(Question, id=question_id)
    else:
        question = None

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        answer_text = request.POST.get('answer_text')
        if question:
            question.question_text = question_text
            question.answer_text = answer_text
            question.save()
        else:
            Question.objects.create(topic=topic, question_text=question_text, answer_text=answer_text)
        return redirect('question_list', topic_id=topic_id)

    return render(request, 'bot/question_edit.html', {'topic': topic, 'question': question})
