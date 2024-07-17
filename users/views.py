from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import paypalrestsdk
from paypalrestsdk import Payment
from django.urls import reverse


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

def process_payment(request):
    selected_plan = request.POST['plan']

    plans = {
        '30' : {'name': 'Ultra light - 30 days', 'price': '2.99'},
        '60' : {'name': 'Popular+ - 60 days', 'price': '3.99'},
        '120': {'name': 'Premium - 120 days', 'price': '4.99'},
    }

    plan_name = plans[selected_plan]['name']
    plan_price = plans[selected_plan]['price']

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')) + '?plan=' + selected_plan,
            "cancel_url": request.build_absolute_uri(reverse('profile'))
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": plan_name,
                    "sku": "item",
                    "price": plan_price,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": plan_price,
                "currency": "USD"},
            "description": f"This is the payment transaction description for {plan_name}."}]})

    if payment.create():
        print('Payment created successfully')
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        print(payment.error)
        return redirect('execute_payment')

def execute_payment(request):
    payment = paypalrestsdk.Payment.find(request.GET['paymentId'])
    selected_plan = request.GET['plan']

    if payment.execute({"payer_id": request.GET['PayerID']}):
        print('Payment executed successfully')
        user_profile = request.user.profile
        user_profile.exp_date = date.today() + timedelta(days=int(selected_plan))
        user_profile.save()
        logout(request)
        return redirect('payment_successful')
    else:
        print(payment.error)

def payment_successful(request):
    return render(request, 'users/payment_successful.html')