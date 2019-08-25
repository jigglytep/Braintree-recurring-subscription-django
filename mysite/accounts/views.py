from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import braintree
import sys, os
import uuid
# import stripe

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=settings.BT_ENVIRONMENT,
        merchant_id=settings.BT_MERCHANT_ID,
        public_key=settings.BT_PUBLIC_KEY,
        private_key=settings.BT_PRIVATE_KEY,
    )
)
plan_id = settings.PLAN_ID

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)


from django.contrib import messages
from django.views.generic.edit import FormView

from django.template.loader import render_to_string

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            customer = gateway.customer.create({
                "email": request.POST['email']
            })
            payment_token = gateway.payment_method.create({
                "customer_id":customer.customer.id,
                "payment_method_nonce": request.POST['payment_method_nonce']
            })
            token = payment_token.payment_method.token
            result = gateway.subscription.create({
                "payment_method_token": token,
                "plan_id": plan_id
            })
            if result.is_success or result.transaction:
                #sign in user
                user = form.save()
                u = User.objects.get(username = user.username)
                u.userprofile.bt_id = token
                u.userprofile.subscription_id = result.subscription.id
                u.userprofile.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                args = {'subscription_status': str(check_status(request)), 'user':u}
                return render(request, 'accounts/profile.html', args)
            else:
                client_token = generate_client_token()
                error = '<ul class="errorlist"><li>Payment Method Declined</li></ul>'
                form = RegistrationForm(request.POST)
                args = {'form': form, 'client_token': client_token, 'error': error}
                return render(request, 'accounts/reg_form.html', args)

        else:
            client_token = generate_client_token()
            error = '<ul class="errorlist"><li>Username is already taken.</li></ul>'
            form = RegistrationForm(request.POST)
            args = {'form': form, 'client_token': client_token, 'error': error }
            return render(request, 'accounts/reg_form.html', args)
    else:
        client_token = generate_client_token()
        form = RegistrationForm(request.POST)
        args = {'form': form, 'client_token': client_token }#
        return render(request, 'accounts/reg_form.html', args)

# @login_required
def view_profile(request):
    args = {'user': request.user, 'subscription_status': check_status(request)}
    return render(request, 'accounts/profile.html', args)

# @login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user )

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
        else:
            form = EditProfileForm(instance=request.user)
            args = {'form': form}
            return render(request, 'accounts/edit_profile.html', args )
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form, 'user':request.user}
        return render(request, 'accounts/edit_profile.html', args )

def cancel_subscription(request):

    instance = request.user

    #TODO: need to add try catch block
    token = instance.userprofile.bt_id
    result = gateway.payment_method.delete(token)
    u = User.objects.get(username = instance.username)
    customer = u.username
    #instead of deleting the user change the username
    #TODO: Add active boolean field.
    u.username = u.username + str(uuid.uuid1)

    u.save()
    logout(request)
    args = {
    'user':customer
    }
    return render(request, 'accounts/cancelled.html', args )

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user )

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/account/change-password')
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args )

def update_card(request):
    if request.method == 'POST':
        try:
            instance = request.user
            customer_id = instance.userprofile.bt_id
            payment_token = gateway.payment_method.update(customer_id,{
                "payment_method_nonce": request.POST['payment_method_nonce']
            })
            args = {'message':"Card updated successfully. Thank you."}
            return render(request, 'accounts/result.html', args )
        except :
            args = {'message':"Sorry something went wrong please try again later or contact us for help."}
            return render(request, 'accounts/result.html', args )

    else:
        client_token = generate_client_token()
        form = RegistrationForm(request.POST)
        args = {'form': form, 'client_token': client_token }#
        return render(request, 'accounts/update.html', args)

def check_status(request):
    username = request.user.username
    user = User.objects.get(username = username)
    subscription = gateway.subscription.find(user.userprofile.subscription_id)
    return subscription.status