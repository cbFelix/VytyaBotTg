from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse_lazy
from functools import wraps

from .forms import UserRegistrationForm, LoginForm
from .models import TgUser, UserMessage, Topic, Question
from .bot_manager import stop_bot, load_state, start_bot


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'bot/register.html', {'form': form, 'error': 'Проверьте введённые данные.'})
    else:
        form = UserRegistrationForm()
    return render(request, 'bot/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'bot/login.html', {'form': form, 'error': 'Неверный email или пароль.'})
        else:
            return render(request, 'bot/login.html', {'form': form, 'error': 'Проверьте введённые данные.'})
    else:
        form = LoginForm()
    return render(request, 'bot/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    return render(request, 'bot/profile.html')


def access_required(level):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.access_level >= level:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()

        return _wrapped_view

    return decorator


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


def index(request):
    bot_status = "running" if load_state() else "stopped"
    return render(request, 'bot/index.html', {'bot_status': bot_status})


def bot_status_view(request):
    bot_status = "running" if load_state() else "stopped"
    return JsonResponse({'status': bot_status})


def bot_settings(request):
    topics = Topic.objects.all()

    if request.method == 'POST':
        if 'create_topic' in request.POST:
            topic_name = request.POST.get('topic_name')
            if topic_name:
                Topic.objects.create(name=topic_name)
                return redirect('bot_settings')
            else:
                return render(request, 'bot/bot_settings.html',
                              {'topics': topics, 'error': 'Название темы не может быть пустым.'})

        if 'create_question' in request.POST:
            topic_id = request.POST.get('topic_id')
            question_text = request.POST.get('question_text')
            answer_text = request.POST.get('answer_text')
            if topic_id and question_text and answer_text:
                topic = get_object_or_404(Topic, id=topic_id)
                Question.objects.create(topic=topic, question_text=question_text, answer_text=answer_text)
                return redirect('bot_settings')
            else:
                return render(request, 'bot/bot_settings.html',
                              {'topics': topics, 'error': 'Заполните все поля для вопроса.'})

    return render(request, 'bot/bot_settings.html', {'topics': topics})


@require_POST
@login_required
def create_topic(request):
    topic_name = request.POST.get('topic_name')
    if topic_name:
        Topic.objects.create(name=topic_name)
    return redirect('bot_settings')


# Редактирование темы
@require_POST
@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    new_topic_name = request.POST.get('new_topic_name')
    if new_topic_name:
        topic.name = new_topic_name
        topic.save()
    return redirect('bot_settings')


# Удаление темы
@require_POST
@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.delete()
    return redirect('bot_settings')


# Добавление вопроса
@require_POST
@login_required
def add_question(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    question_text = request.POST.get('question_text')
    answer_text = request.POST.get('answer_text')
    if question_text and answer_text:
        Question.objects.create(topic=topic, question_text=question_text, answer_text=answer_text)
    return redirect('bot_settings')


# Редактирование вопроса
@require_POST
@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question_text = request.POST.get('question_text')
    answer_text = request.POST.get('answer_text')
    if question_text and answer_text:
        question.question_text = question_text
        question.answer_text = answer_text
        question.save()
    return redirect('bot_settings')


# Удаление вопроса
@require_POST
@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('bot_settings')


def bot_settings(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        if 'create_topic' in request.POST:
            return create_topic(request)
        elif 'create_question' in request.POST:
            return add_question(request)
        elif 'edit_topic' in request.POST:
            topic_id = request.POST.get('topic_id')
            return edit_topic(request, topic_id)
        elif 'delete_topic' in request.POST:
            topic_id = request.POST.get('topic_id')
            return delete_topic(request, topic_id)
        elif 'edit_question' in request.POST:
            question_id = request.POST.get('question_id')
            return edit_question(request, question_id)
        elif 'delete_question' in request.POST:
            question_id = request.POST.get('question_id')
            return delete_question(request, question_id)
    return render(request, 'bot/bot_settings.html', {'topics': topics})
