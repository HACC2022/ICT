from django.urls import path
from . import views
#URL Config
urlpatterns = [
    path('', views.hello, name='index'),
    path('shorten', views.shorten, name='shorten'),
    path('manage/search', views.search_view, name="search"),
    path('<str:pk>', views.forward, name='forward'),
    path('manage/', views.manage_view, name='manage'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('delete/<pk>/', views.manage_view_delete, name='delete_data')
]