# scanner/urls.py

from django.urls import path
from authentication import views
from scanner import views
from .views import index, scan, download, cve_descriptor
from .views import scan_form_view, scan_result_view


urlpatterns = [
    path('index/', index, name='index'),
    path('scan/', scan, name='scan'),
    path('download/', download, name='download'),
    path('cve-descriptor/', cve_descriptor, name='cve_descriptor'),
    path('scan-tool/', views.scan_tool, name='scan_tool'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    # path('dirscan/', views.scan_subdomains, name='scan_subdomains'),
    path('dirscan/', scan_form_view, name='scan_form'),
    path('result/<int:result_id>/', scan_result_view, name='scan_result'),
]
