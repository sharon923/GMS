from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import packages, history, user_member, delivery_status
from .forms import SignupForm
from .common.forms import LoginForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from datetime import datetime


def index(request):
    pack = packages.objects.all()
    context = {'details': pack}
    if (request.user.is_authenticated):
        if request.user.is_superuser:
            return redirect('/admin')
        else:    
            return redirect('/home', {"company_info": True})
    return render(request,'./myapp/index.html',context)

def price(request):
    pack = packages.objects.all()
    context = {'details': pack}
    return render(request, './myapp/price.html', context)

def price_details(request):
    id = request.GET.get('id')
    print(id)
    up = packages.objects.get(id=int(id))
    context = {'up': up}
    return render(request, './myapp/price_details.html',context)

def subscribe(request):
    return render(request, './myapp/subscribe.html')
