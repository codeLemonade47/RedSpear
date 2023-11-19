from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('home', views.home, name='home'),
    path('fullscan', views.fullscan, name='fullscan'),
    path('login/', views.loginuser, name='loginuser'),
    path("download/", views.download_file, name="download_file"),
    path("logout/", views.logoutuser, name="logoutuser"),
    path("cvedes/", views.cvedes, name="cvedes"),
]