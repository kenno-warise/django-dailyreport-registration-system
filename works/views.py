from django.shortcuts import render


def login(request):
    return render(request, 'works/login.html')


def index(request):
    return render(request, 'works/index.html')


def admin_login(request):
    return render(request, 'works/admin_login.html')


def user_list(request):
    return render(request, 'works/user_list.html')


def user_result(request):
    return render(request, 'works/user_result.html')

# Create your views here.
