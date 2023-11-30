from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.generic.base import View

from utils.email_service import send_email

from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from .models import User


class RegisterView(View):
    def get(self, request: HttpRequest):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request, 'account/register.html', context)

    def post(self, request: HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email)

            if user:
                register_form.add_error('email', 'پست الکترونیکی تکراری می باشد.')
            else:
                new_user = User(email=user_email, email_active_code=get_random_string(85), is_active=False)
                new_user.set_password(user_password)
                new_user.save()
                send_email('اوتو پارت-فعال سازی حساب کاربری', new_user.email, {'user': new_user},
                           'core/email/account_activation.html')
                messages.success(request, 'ثبت نام با موفقیت انجام شد. لطفا وارد حساب کاربری خود شوید.')
                return redirect('login')

        context = {'register_form': register_form}
        return render(request, 'account/register.html', context)


class AccountActivationView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(90)
                user.save()
                messages.success(request, 'حساب کاربری شما با موفقیت فعال شد.')
                return redirect('login')

        raise Http404()


class LoginView(View):
    def get(self, request: HttpRequest):
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'account/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            is_remember = login_form.cleaned_data.get('remember_me')

            if is_remember:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)

            user: User = User.objects.filter(email__iexact=user_email).first()

            if user:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نمی باشد.')
                else:
                    is_correct_password = user.check_password(user_password)
                    if is_correct_password:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        if 'next' in request.POST:
                            return redirect(request.POST.get('next'))
                        else:
                            greeting = lambda \
                                    user: f'{user.first_name if user.first_name else "کاربر"} عزیز. خوش آمدید.'
                            messages.success(request, greeting(user))
                            return redirect('home')
                    else:
                        login_form.add_error('email', 'کاربری با اطلاعات وارد شده یافت نشد.')
            else:
                login_form.add_error('email', 'کاربری با اطلاعات وارد شده یافت نشد.')

        context = {'login_form': login_form}
        return render(request, 'account/login.html', context)


class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        messages.error(request, 'شما از حساب کاربری خود خارج شدید.')
        return redirect('login')


class ForgetPasswwordView(View):
    def get(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm()
        context = {'forget_password_form': forget_password_form}
        return render(request, 'account/forget_password.html', context)

    def post(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            user_email = forget_password_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()

            if user:
                send_email('اوتو پارت-بازیابی کلمه عبور', user.email, {'user': user},
                           'core/email/reset_password.html')
                messages.info(request, 'ایمیل بازیابی کلمه عبور برای شما ارسال شد. لطفا ایمیل خود را بررسی کنید.')
                return redirect('home')
            else:
                forget_password_form.add_error('email',
                                               'کاربرگرامی، شما ثبت نام نکرده اید یا حساب کاربری شما فعال نمی باشد.')

        context = {'forget_password_form': forget_password_form}
        return render(request, 'account/forget_password.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        reset_password_form = ResetPasswordForm()
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        context = {'reset_password_form': reset_password_form, 'user': user}
        return render(request, 'account/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            new_password = reset_password_form.cleaned_data.get('password')
            user: User = User.objects.filter(email_active_code__iexact=active_code).first()

            if user:
                user.set_password(new_password)
                user.is_active = True
                user.email_active_code = get_random_string(90)
                user.save()
                messages.success(request, 'کلمه عبور با موفقیت تغییر یافت. حال می توانید وارد حساب کاربری خود شوید.')
                return redirect('login')
            else:
                raise Http404()

        context = {'reset_password_form': reset_password_form}
        return render(request, 'account/reset_password.html', context)
