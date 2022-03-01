import requests
from django.shortcuts import render, redirect
from apps.API.models import Customer, Contract, Event
from django.contrib.auth.views import LoginView as BaseLogin
from django.contrib.auth.decorators import login_required
import requests


class LoginView(BaseLogin):
    """
    Overriding Django default login view to get JWT from api at login and
    storing them as cookies
    """

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


# TODO: delete cookies at logout


@login_required
def home(request):
    return render(request, 'front/home.html')


# TODO: appel api avec JS...


@login_required
def customers(request):
    token = request.COOKIES.get('access')
    endpoint = 'http://127.0.0.1:8000/api/customers/'
    head = {'Authorization': 'Bearer ' + token}
    data = requests.get(endpoint, headers=head).json()
    context = {'clients': data['results']}
    return render(request, 'front/customers.html', context)


def contracts(request):
    token = request.COOKIES.get('access')
    endpoint = 'http://127.0.0.1:8000/api/contracts/'
    head = {'Authorization': 'Bearer ' + token}
    data = requests.get(endpoint, headers=head).json()
    context = {'contracts': data['results']}
    return render(request, 'front/contracts.html', context)


def events(request):
    token = request.COOKIES.get('access')
    endpoint = 'http://127.0.0.1:8000/api/events/'
    head = {'Authorization': 'Bearer ' + token}
    data = requests.get(endpoint, headers=head).json()
    context = {'events': data['results']}
    return render(request, 'front/events.html', context)


def account(request):
    pass


def projects(request):
    pass
