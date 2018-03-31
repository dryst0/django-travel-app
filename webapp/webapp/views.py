from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render

@login_required(login_url='/login/')
def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return render(request, "login.html")

def login_user(request):
    if request.POST:
        username = request.POST['inputUsername']
        password = request.POST['inputPassword']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')

    return render(request, "login.html")

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)

    return render(request, "login.html")
