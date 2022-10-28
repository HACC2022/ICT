import re
from django.shortcuts import get_object_or_404, render, redirect
import uuid
from .models import Url
from django.http import HttpResponse

# Create your views here.
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

def manage_view(request, id):
    queryset = Url.objects.all()
    context = {
        'object_list': queryset
    }
    return render (request, 'manage.html', context)