# scanner/urls.py

# from django.urls import path
# from authentication import views
# from scanner import views
# from .views import index, scan, download, cve_descriptor, scan_tool, download_pdf, scan_form_view, scan_result_view
# from django.contrib.auth.decorators import login_required


# urlpatterns = [
#     path('index/', login_required(index), name='index'),
#     path('scan/', login_required(scan), name='scan'),
#     path('download/', login_required(download), name='download'),
#     path('cve-descriptor/', login_required(cve_descriptor), name='cve_descriptor'),
#     path('scan-tool/', login_required(views.scan_tool), name='scan_tool'),
#     path('download-pdf/', login_required(views.download_pdf), name='download_pdf'),
#     # path('dirscan/', views.scan_subdomains, name='scan_subdomains'),
#     path('dirscan/', login_required(scan_form_view), name='scan_form'),
#     path('result/<int:result_id>/', login_required(scan_result_view), name='scan_result'),
# ]


from django.urls import path
from authentication import views as auth_views
from scanner import views as scanner_views
from .views import index, scan, download, cve_descriptor, scan_form_view, scan_result_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('index/', login_required(index), name='index'),
    path('scan/', login_required(scan), name='scan'),
    path('download/', login_required(download), name='download'),
    path('cve-descriptor/', login_required(cve_descriptor), name='cve_descriptor'),
    path('scan-tool/', login_required(scanner_views.scan_tool), name='scan_tool'),
    path('download-pdf/', login_required(scanner_views.download_pdf), name='download_pdf'),
    # path('dirscan/', views.scan_subdomains, name='scan_subdomains'),
    path('dirscan/', login_required(scan_form_view), name='scan_form'),
    path('result/<int:result_id>/', login_required(scan_result_view), name='scan_result'),
    path('logout/', LogoutView.as_view(), name='logout'),

]