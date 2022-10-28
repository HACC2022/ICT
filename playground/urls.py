from django.urls import path
from . import views
#URL Config
urlpatterns = [
    path('', views.hello),
    path('shorten', views.shorten, name='shorten'),
    path('<str:pk>', views.forward, name='forward'),
    path('manage/', views.manage_view, name='manage')
]