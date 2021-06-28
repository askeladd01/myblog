import string
import time
import random
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail

from . import myforms
from .models import Profile


# Create your views here.
def login(request):
    if request.method == 'POST':
        login_obj = myforms.LoginForm(request.POST)
        if login_obj.is_valid():
            user = login_obj.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_obj = myforms.LoginForm()
    return render(request, 'user/login.html', {'login_obj': login_obj})


def login_for_modal(request):
    login_obj = myforms.LoginForm(request.POST)
    data = {}
    if login_obj.is_valid():
        user = login_obj.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        reg_obj = myforms.RegForm(request.POST, request=request)
        if reg_obj.is_valid():
            username = reg_obj.cleaned_data['username']
            password = reg_obj.cleaned_data['password']
            email = reg_obj.cleaned_data['email']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            del request.session['register_code']

            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_obj = myforms.RegForm()
    return render(request, 'user/register.html', {'reg_obj': reg_obj})


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    return render(request, 'user/user_info.html')


def change_nickname(request):
    redirect_url = request.GET.get('from', reverse('home'))
    context = {}
    if request.method == 'POST':
        form_info = myforms.ChangeNicknameForm(request.POST, user=request.user)
        if form_info.is_valid():
            new_nickname = form_info.cleaned_data['new_nickname']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = new_nickname
            profile.save()
            return redirect(redirect_url)
    else:
        form_info = myforms.ChangeNicknameForm()

    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form_info
    context['redirect_url'] = redirect_url

    return render(request, 'forms.html', context)


def bind_email(request):
    redirect_url = request.GET.get('from', reverse('home'))
    context = {}
    if request.method == 'POST':
        form_info = myforms.BindEmailForm(request.POST, request=request)
        if form_info.is_valid():
            email = form_info.cleaned_data['email']
            request.user.email = email
            request.user.save()

            del request.session['email_code']
            return redirect(redirect_url)
    else:
        form_info = myforms.BindEmailForm()

    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form_info
    context['redirect_url'] = redirect_url

    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for')
    data = {}
    if email:
        code = ''.join(random.sample(string.ascii_letters+string.digits, 6))
        send_time = request.session.get('send_time', 0)
        if time.time() - send_time < 30:
            data['status'] = 'ERROR_time'
        else:
            request.session[send_for] = code
            request.session['send_time'] = time.time()
            send_mail('绑定邮箱', f'验证码:{code}', '1073418959@qq.com', [email], fail_silently=False,)
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(request):
    redirect_url = reverse('home')
    context = {}
    if request.method == 'POST':
        form_info = myforms.ChangePasswordForm(request.POST, user=request.user)
        if form_info.is_valid():
            user = request.user
            password = form_info.cleaned_data['password']
            user.set_password(password)
            user.save()

            auth.logout(request)
            return redirect(redirect_url)
    else:
        form_info = myforms.ChangePasswordForm()

    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form_info
    context['redirect_url'] = redirect_url

    return render(request, 'forms.html', context)


def forget_password(request):
    redirect_url = reverse('home')
    context = {}
    if request.method == 'POST':
        form_info = myforms.ForgetPasswordForm(request.POST, request=request)
        if form_info.is_valid():
            email = form_info.cleaned_data['email']
            password = form_info.cleaned_data['password']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

            del request.session['forget_password_code']
            return redirect(redirect_url)
    else:
        form_info = myforms.ForgetPasswordForm()

    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form_info
    context['redirect_url'] = redirect_url

    return render(request, 'user/forget_psd.html', context)