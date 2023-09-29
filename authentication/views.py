from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def signin(request):
    return render(request, "authentication/signin.html")

def signup(request):
    username = request.POST['username']
    password = request.POST['password']

    myuser = User.objects.create_user(username, password)
    myuser.save()

    messages.success(request, "You're now the user.")

    return redirect('signin')









    return render(request, "authentication/signup.html")

def home(request):
    pass

def signout(request):
    pass

def dashboard(request):
    return render(request, "toolkit/dashboard.html")