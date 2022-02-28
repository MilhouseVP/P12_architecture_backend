import json

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.views import LoginView as BaseLogin
from django.contrib.auth.decorators import login_required
import requests


class LoginView(BaseLogin):
    def form_valid(self, form):
        response = super().form_valid(form)
        endpoint = 'http://127.0.0.1:8000/api/login/'
        username = form['username'].value()
        password = form['password'].value()
        data = {'username': username, 'password': password}
        tokens = requests.post(url=endpoint, data=data).json()
        response.set_cookie('access', tokens['access'])
        response.set_cookie('refresh', tokens['refresh'])
        return response



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
