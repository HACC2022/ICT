import re
from django.shortcuts import get_object_or_404, render, redirect
import uuid

import pkg_resources
from .models import Url
from django.http import HttpResponse, JsonResponse
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

def manage_view(request):
    queryset = Url.objects.all()
    context = {
        'object_list': queryset
    }
    return render (request, 'manage.html', context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def manage_view_delete(request, pk, *args, **kwargs):
    if is_ajax(request):
        obj = Url.objects.get(pk=pk)
        obj.delete()
        return JsonResponse({"message":"success"})
    return JsonResponse({"message":"Something is wrong"})

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
