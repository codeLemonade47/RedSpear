# scanner/urls.py

from django.urls import path
from authentication import views
from .views import index, scan, download

urlpatterns = [
    path('index/', index, name='index'),
    path('scan/', scan, name='scan'),
    path('download/', download, name='download'),
    path('dashboard', views.dashboard, name='dashboard'),
]
