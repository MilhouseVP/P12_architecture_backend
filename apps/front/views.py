from django.shortcuts import render, redirect
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

def api_mixin(request, endpoint):
    token = request.COOKIES.get('access')
    head = {'Authorization': 'Bearer ' + token}
    data = requests.get(endpoint, headers=head).json()
    return data


@login_required
def home(request):
    return render(request, 'front/home.html')


# TODO: appel api avec JS...


@login_required
def customers(request):
    endpoint = 'http://127.0.0.1:8000/api/customers/'
    data = api_mixin(request, endpoint)
    context = {'clients': data['results']}
    return render(request, 'front/customers.html', context)


@login_required
def customer(request, customer_id):
    endpoint = 'http://127.0.0.1:8000/api/customers/' + str(customer_id) + '/'
    data = api_mixin(request, endpoint)
    context = {'customer': data}
    return render(request, 'front/customer_details.html', context)

def contracts(request):
    endpoint = 'http://127.0.0.1:8000/api/contracts/'
    data = api_mixin(request, endpoint)
    context = {'contracts': data['results']}
    return render(request, 'front/contracts.html', context)


def events(request):
    endpoint = 'http://127.0.0.1:8000/api/events/'
    data = api_mixin(request, endpoint)
    context = {'events': data['results']}
    return render(request, 'front/events.html', context)


def account(request):
    pass


def projects(request):
    pass
