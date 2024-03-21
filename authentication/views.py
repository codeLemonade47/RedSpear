import multiprocessing
import os
import re


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import Http404, HttpResponse, StreamingHttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


from .forms import(
    IpscanForm, CvedesForm
)

from templates.scripts import nmap, fullscan, cvescanner

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
def signin(request):
    if request.method == 'POST':
        # Get the form data
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Redirect to a success page
            return redirect('dashboard')
        else:
            # Return an 'invalid login' error message
            return render(request, 'authentication/signin.html', {'error': 'Invalid login'})

    # If the request is not a POST, render the login form
    return render(request, 'authentication/signin.html')

def signup(request):
    if request.method == 'POST':
        # Get the form data
        username = request.POST['username']
        password = request.POST['password']

        # Create a new user with the form data
        User.objects.create_user(username=username, password=password)

        # Redirect to a success page
        return redirect('signin')

    # If the request is not a POST, render the signup form
    return render(request, 'authentication/signup.html')

@login_required
def home(request):
    return render(request, 'toolkit/home.html')

@login_required
def signout(request):
    pass

@login_required
def dashboard(request):
    return render(request, "toolkit/dashboard.html")


def fullscan(request):
    if request.method == "GET":
        return render(request, "toolkit/fullscan.html", {"form": IpscanForm()})
    else:
        try:
            global ip, user_name, function_name
            form = IpscanForm(request.POST)
            if form.is_valid():
                ip = form.cleaned_data['ip']
                function_name = "fullscan"
                user_name = request.user
                p_fullscan = multiprocessing.Process(
                    target = nmap.nmap_script,
                    args=(
                        ip,
                        user_name,
                        function_name
                    ),
                )
                p_fullscan.start()
                p_fullscan.join()

        except ValueError:
            return render(
                request,
                "toolkit/dashboard.html",
                {"error": "Bad data passed in. Try again."}
            )
    
    return render(request, "toolkit/download.html")

@login_required
def loginuser(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "toolkit/dashboard.html")
        

@login_required
def download_file(request):
    filename = f"{function_name}-{ip}.pdf"
    user_name = request.user
    filepath = f"{BASE_DIR}/toolkit/media/toolkit/reports/{user_name}/{filename}"

    if os.path.exists(filepath):
        response = HttpResponse(open(filepath, "rb"))
        response["Content-Disposition"] = "attachment; filename=%s" % filename
        return response
    else:
        raise Http404
    

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("signin")
    else:
        return redirect("signin")
    
@login_required
def forbidden(request):
    if request.method == "GET":
        return render(request, "toolkit/403.html")

  
def cvedes(request):
    if request.method == "GET":
        return render(request, "toolkit/cvedes.html", {"form": CvedesForm()})

    else:
        try:
            global cve_id, user_name
            form = CvedesForm(request.POST)
            if form.is_valid():
                cve_id = form.cleaned_data.get("cve_id")
                cve_id = f"cve-{cve_id}" if not cve_id.startswith("cve-") else cve_id
                user_name = request.user
                result = cvescanner.cve_search(cve_id)
                if result is None:
                    return render(
                        request,
                        "toolkit/cvedes.html",
                        {"error": "The requested CVE-ID cannot be found."},
                    )
                else:
                    context = {"result": result}
                    return render(request, "toolkit/cvedes.html", context)

        except ValueError:
            return render(
                request,
                "toolkit/cvedes.html",
                {"error": "Bad data passed in. Try again."},
            )