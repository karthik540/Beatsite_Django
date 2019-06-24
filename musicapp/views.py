from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login , logout
from .models import CustomUser
# Create your views here.

def index(request):
    return render(request , 'index.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.get(email = email)

        if user is not None:
            if user.check_password(password):
                if user.is_active:
                    login(request , user)
                    return JsonResponse({'flag' : 1})
    return JsonResponse({'flag' : 0})

def logout_user(request):
    logout(request)
    return JsonResponse({'flag' : 1})

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = CustomUser()
        user.username = username
        user.password = password
        user.email = email
        user.save()

        user = CustomUser.objects.get(email = email)
        print(user)
        if user is not None:
            login(request , user)
            return JsonResponse({'flag' : 1})
    return JsonResponse({'flag' : 0})


