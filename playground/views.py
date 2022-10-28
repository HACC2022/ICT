import re
from django.shortcuts import render, redirect
import uuid
from .models import Url
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url= 'login')
def hello(request):
    return render (request, 'index.html', {'name': 'zeek'})

def shorten(request):
    if request.method == 'POST':
        lURL = request.POST['link']
        sCode = str(uuid.uuid4())[:5]
        shortUrl = Url(longLink=lURL,shortCode=sCode)
        shortUrl.save()
        return HttpResponse(sCode)

def forward(request, pk):
    long_url = Url.objects.get(shortCode=pk)
    return redirect(long_url.longLink)


def loginPage(request):
   
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,'Username or Password incorrect')
            return redirect('login')
    context={}
    return render (request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')