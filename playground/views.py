from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
import uuid
import requests

import pkg_resources
from django.template.loader import render_to_string

from .models import Url, IP_Adresses
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login')
def hello(request):
    return render(request, 'index.html', {'name': 'zeek'})


@login_required(login_url='login')
def shorten(request):
    if request.method == 'POST':
        lURL = request.POST['link']
        if ".gov" not in lURL:
            return HttpResponse("error")
        sCode = str(uuid.uuid4())[:5]
        shortUrl = Url(longLink=lURL, shortCode=sCode)
        shortUrl.save()
        return HttpResponse("https://etsurl.com/" + sCode)


def forward(request, pk):
    long_url = Url.objects.get(shortCode=pk)
    long_url.clicks += 1
    long_url.save()
    ip = get_client_ip(request)
    ip_origin = IP_Adresses(shortCode=long_url, ip_address=ip)
    ip_origin.save()
    return redirect(long_url.longLink)


@login_required(login_url='login')
def manage_view(request):
    queryset = Url.objects.all()
    ipset = IP_Adresses.objects.all()
    print(ipset)
    context = {
        'object_list': queryset,
        'ipset_list': ipset,
    }
    return render(request, 'manage.html', context)


@login_required(login_url='login')
def search_view(request):
    if request.method == 'POST':
        word = request.POST['keyword']
        queryset = Url.objects.filter(longLink__icontains=word)
        context = {
            'object_list': queryset
        }
        html = render_to_string('search_result.html', context)
        return JsonResponse(html, safe=False)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='login')
def manage_view_delete(request, pk, *args, **kwargs):
    if is_ajax(request):
        obj = Url.objects.get(pk=pk)
        obj.delete()
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "Something is wrong"})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password incorrect')
            return redirect('login')
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required(login_url='login')
def get_status(request, pk):
    longUrl = Url.objects.get(pk=pk)
    s = longUrl.status
    r = requests.head(longUrl.longLink)
    status_code = r.status_code
    if (status_code == 200):
        longUrl.status = "Good"
        longUrl.save()
        return HttpResponseRedirect(reverse('manage'))
    else:
        longUrl.status = "Bad"
        longUrl.save()
        return HttpResponseRedirect(reverse('manage'))
