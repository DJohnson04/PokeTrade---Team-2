from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.urls import reverse_lazy

from .forms import WalletForm

from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import UserAccount


# Create your views here.
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
import logging

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        logging.info("Password reset form is valid. Sending email.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logging.error(f"Password reset form is invalid: {form.errors}")
        return super().form_invalid(form)

def wallet_view(request):
    owned_profile = UserAccount.objects.get(user=request.user)
    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            action = form.cleaned_data['action']
            if action == 'deposit':
                owned_profile.wallet += amount
            elif action == 'withdraw' and owned_profile.wallet >= amount:
                owned_profile.wallet -= amount
            owned_profile.save()
            return redirect('accounts:wallet')
    else:
        form = WalletForm()
    return render(request, 'accounts/wallet.html', {'form': form, 'wallet': owned_profile.wallet})