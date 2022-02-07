from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'front/home.html')
