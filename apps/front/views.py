from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'front/home.html')

# TODO: appel api avec JS...


@login_required
def customers(request):
    pass

def contracts(request):
    pass

def events(request):
    pass

def account(request):
    pass

def projects(request):
    pass
