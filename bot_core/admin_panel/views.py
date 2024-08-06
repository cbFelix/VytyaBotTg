from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Idi nahui suka")


def users(request):
    return HttpResponse("Users")


def bot_menu(request):
    return HttpResponse("Bot menu")


def cli_menu(request):
    return HttpResponse("Cli")
