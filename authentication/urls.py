# from django.contrib import admin
# from django.urls import include, path
# from . import views
# from .views import signup, signin, signout, dashboard, home, fullscan, logoutuser, cvedes
# from django.contrib.auth.decorators import login_required

# urlpatterns = [
#     path('signup/', views.signup, name='signup'),
#     path('signin/', views.signin, name='signin'),
#     path('signout', login_required(views.signout), name='signout'),
#     path('dashboard', login_required(views.dashboard), name='dashboard'),
#     path('home', login_required(views.home), name='home'),
#     path('fullscan', login_required(views.fullscan), name='fullscan'),
#     path('login/', views.loginuser, name='loginuser'),
#    # path("download/", views.download_file, name="download_file"),
#     path("logout/", login_required(views.logoutuser), name="logoutuser"),
#     path("cvedes/", login_required(views.cvedes), name="cvedes"),

# ]


from django.contrib import admin
from django.urls import include, path
from . import views
from .views import signup, signin, dashboard, home, fullscan, logoutuser, cvedes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout', login_required(views.signout), name='signout'),
    path('dashboard', login_required(views.dashboard), name='dashboard'),
    path('home/', login_required(views.home), name='home'),
    path('fullscan', login_required(views.fullscan), name='fullscan'),
    path('login/', views.loginuser, name='loginuser'),
    path("logoutuser/", login_required(views.logoutuser), name="logoutuser"),
    path("cvedes/", login_required(views.cvedes), name="cvedes"),
    # path('logout/', LogoutView.as_view(), name='logout'),
]