from django.shortcuts import render

from django.http import HttpResponse
def index(request):
 return HttpResponse('Главная страница электронного журнала.')

from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница электронного журнала.')


def about(request):
    return HttpResponse('О проекте: электронный журнал посещаемости.')