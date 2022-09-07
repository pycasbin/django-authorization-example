import hashlib
import os
import sys

from dauthz.core import enforcer
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from . import forms

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def hash_code(s, salt='sad122sad'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    # now_user_name = request.session.get('user_name', None)
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    # user.
    all_users = User.objects.all()
    user_name_list = []
    for u in all_users:
        user_name_list.append(u.username)
    return render(request, 'index.html', locals())


def login(request):
    if request.session.get("is_login", None):
        return redirect('/')
    message = None
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        message = "please check your input!"
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            is_user_exist = User.objects.filter(username=username).exists()
            if is_user_exist:
                user = auth.authenticate(request, username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/')
                else:
                    message = "password wrong"
            else:
                message = "user is not exist"
    login_form = forms.LoginForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get("is_login", None):
        return redirect('/')
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "please check your input!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')

            if password1 != password2:
                message = 'password is not same!'
                return render(request, 'register.html', locals())
            else:
                is_user_exist = User.objects.filter(username=username).exists()
                if is_user_exist:
                    message = 'user already exist!'
                    return render(request, 'register.html', locals())
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                enforcer.add_policy(username, "/user/"+username, "GET")
                enforcer.add_role_for_user(username, "normal_user")
                return redirect('/login')
        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login')
    request.session.flush()
    return redirect('/login')


def user_profile(request, user_name):
    user = User.objects.get(username=user_name)
    return render(request, 'user_profile.html', locals())


def all_users_profile(request):
    users = User.objects.all()
    return render(request, 'all_users_profile.html', locals())
