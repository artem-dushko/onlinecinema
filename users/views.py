from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} has been created! Now you can login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form    = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Profile details have been updated.')
            return redirect('profile')
    else:
        user_update_form    = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)  

        exp_date = request.user.profile.exp_date
        is_expired = exp_date < date.today()

    context = {
        'u_form': user_update_form,
        'p_form': profile_update_form,
        'is_expired': is_expired,
        'exp_date': exp_date
    }
    return render(request, 'users/profile.html', context)

def user_logout(request):
    logout(request)
    return render(request, 'users/logout.html')

def subscription(request):
    if request.user.profile.exp_date > date.today():
        return redirect('profile')
    return render(request, 'users/subscription.html')

def process_subscription(request):
    plan = request.POST['plan']
    user_profile = request.user.profile
    user_profile.exp_date = date.today() + timedelta(days=int(plan))
    user_profile.save()
    return redirect('cinema-home')

@receiver(user_logged_in)
def update_profile(sender, user, request, **kwargs):
    profile = user.profile
    profile.is_expired = profile.exp_date < date.today()
    profile.save()