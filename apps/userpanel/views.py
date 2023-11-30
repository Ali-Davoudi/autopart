from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from .forms import EditUserForm, ChangeUserPasswordForm

from apps.account.models import User
from apps.basket_order.models import UserBasketOrder, UserBasketOrderDetail


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardView(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_user_form = EditUserForm(instance=current_user)
        change_user_password_form = ChangeUserPasswordForm()
        user_basket_order = UserBasketOrder.objects.filter(user_id=request.user.id, is_paid=False).first()
        paid_user_basket_orders = UserBasketOrderDetail.objects.filter(
            user_basket_order__is_paid=True, user_basket_order__user_id=request.user.id)

        context = {
            'current_user': current_user,
            'edit_user_form': edit_user_form,
            'change_user_password_form': change_user_password_form,
            'user_basket_order': user_basket_order,
            'paid_user_basket_orders': paid_user_basket_orders
        }
        return render(request, 'userpanel/user_panel_dashboard.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_user_form = EditUserForm(request.POST, request.FILES, instance=current_user)
        if edit_user_form.is_valid():
            edit_user_form.save(commit=True)
            messages.success(request, 'ویرایش اطلاعات با موفقیت انجام شد.')
            return redirect('dashboard')

        change_user_password_form = ChangeUserPasswordForm(request.POST)
        if change_user_password_form.is_valid():
            current_password = change_user_password_form.cleaned_data.get('current_password')
            new_password = change_user_password_form.cleaned_data.get('new_password')

            is_correct_password = current_user.check_password(current_password)
            if is_correct_password:
                current_user.set_password(new_password)
                current_user.save(update_fields=['password'])
                logout(request)
                messages.info(request, 'کلمه عبور با موفقیت تغییر یافت.')
                return redirect('login')

            else:
                change_user_password_form.add_error('current_password', 'کلمه عبور جاری صحیح نمی باشد.')

        context = {
            'current_user': current_user,
            'edit_user_form': edit_user_form,
            'change_user_password_form': change_user_password_form
        }
        return render(request, 'userpanel/user_panel_dashboard.html', context)
