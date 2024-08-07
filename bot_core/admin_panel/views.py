from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(
        request,
        'bot/index.html',
        {

        },
    )


def users(request):
    return render(
        request,
        'bot/users.html',
        {

        },
    )


def bot_menu(request):
    return render(
        request,
        'bot/bot_menu.html',
        {

        },
    )


def cli_menu(request):
    return render(
        request,
        'bot/cli_menu.html',
        {

        },
    )