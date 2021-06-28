from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱',
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': '请输入用户名或邮箱'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '请输入密码'}))

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=3, max_length=10,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '请输入3-10位用户名'}))
    password = forms.CharField(label='密码', min_length=8, max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '请输入8-32位密码'}))
    re_password = forms.CharField(label='确认密码', min_length=8, max_length=32,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': '请确认密码'}))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
                             error_messages={'required': '邮箱还没有填写哦~'})
    verification_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        error_messages={'required': '验证码还没有填写哦~'})

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_re_password(self):
        password = self.cleaned_data['password']
        re_password = self.cleaned_data['re_password']
        if password != re_password:
            raise forms.ValidationError('两次输入的密码不一致')
        return re_password

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被绑定')
        return email

    def clean_verification_code(self):
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code')
        if code and code == verification_code:
            return verification_code
        else:
            raise forms.ValidationError('验证码错误')


class ChangeNicknameForm(forms.Form):
    new_nickname = forms.CharField(label='新的昵称', max_length=10,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}),
                                   error_messages={'required': '新昵称不能为空'})

    # 判断用户是否已经登录
    # 首先通过form自带的双下init方法尝试获取用户信息
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 如果有用户信息则添加到验证数据中，没有则报错
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')

        return self.cleaned_data


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    verification_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        error_messages={'required': '验证码还没有填写哦~'})

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean_verification_code(self):
        code = self.request.session.get('email_code', '')
        verification_code = self.cleaned_data.get('verification_code')
        if code and code == verification_code:
            return verification_code
        else:
            raise forms.ValidationError('验证码错误')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被绑定')
        return email


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='原密码', min_length=8, max_length=32,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': '请输入8-32位密码'}))
    password = forms.CharField(label='新密码', min_length=8, max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '请输入8-32位密码'}))
    re_password = forms.CharField(label='确认密码', min_length=8, max_length=32,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': '请确认密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_re_password(self):
        password = self.cleaned_data['password']
        re_password = self.cleaned_data['re_password']
        if password != re_password:
            raise forms.ValidationError('两次输入的密码不一致')
        return re_password

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码不正确')
        return old_password


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入注册邮箱'}),
                             error_messages={'required': '邮箱还没有填写哦~'})
    verification_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        error_messages={'required': '验证码还没有填写哦~'})
    password = forms.CharField(label='新密码', min_length=8, max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '请输入8-32位新密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱不存在')
        return email

    def clean_verification_code(self):
        code = self.request.session.get('forget_password_code', '')
        verification_code = self.cleaned_data.get('verification_code')
        if code and code == verification_code:
            return verification_code
        else:
            raise forms.ValidationError('验证码错误')
