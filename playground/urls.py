from django.urls import path
from . import views
#URL Config
urlpatterns = [
    path('', views.hello, name='index'),
    path('shorten', views.shorten, name='shorten'),
    path('<str:pk>', views.forward, name='forward'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logoutUser')
]