from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import FormView
from accountprofile.forms import UserUpdateForm, ProfileUpdateForm, PackageForm, PaidForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from diamond.models import UserProfile

from accountprofile.models import Package
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from python_paystack.objects.transactions import Transaction
from python_paystack.managers import TransactionsManager


class IndexView(TemplateView):
    template_name = "index.html"


class DashboardView(TemplateView):
    template_name = "profile/dashboard.html"

    def get_context_data(self, **kwargs):
        queryset = UserProfile.objects.order_by('referree')
        context = super().get_context_data(**kwargs)
        context['queryset'] = queryset
        return context


class AccountView(TemplateView):
    template_name = "profile/profile.html"


class PackageListView(ListView):

    context_object_name = 'queryset'
    queryset = Package.objects.order_by('price')
    form_class = PackageForm
    template_name = 'profile/package.html'
    success_url = reverse_lazy('package')

    def get_context_data(self, **kwargs):
        queryset = Package.objects.order_by('price')
        context = super().get_context_data(**kwargs)
        context['queryset'] = queryset
        return context

    def post(self, request, *args, **kwargs):
        pa_form = PackageForm(
            self.request.POST, instance=request.user.userprofile)

        if pa_form.is_valid():
            pa_form.save()
            return redirect('package')
        else:
            return self.form_invalid(pa_form, **kwargs)


@login_required
def edit_profile(request):
    queryset = Package.objects.order_by('price')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('edit_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'queryset': queryset,
    }

    return render(request, 'profile/update.html', context)


def make_payment(request, id):

    current_user = request.user
    shopcart = UserProfile.objects.filter(user_id=current_user.id)
    total = 0

    for rs in shopcart:
        total += rs.package.price

    email = request.user.email
    packageid = request.user.userprofile.package.id

    if id == packageid:
        transaction = Transaction(total * 100 + 1000, email)

    data = json.JSONDecoder().decode(transaction.to_json())

    transaction_manager = TransactionsManager()
    transaction = transaction_manager.initialize_transaction(
        'STANDARD', transaction, callback_url="http://localhost:8000/user/paid/")
    return redirect(transaction.authorization_url)


@login_required
def check_payment(request):
    user = request.user

    if request.method == "POST":
        form = PaidForm(request.POST,
                        instance=request.user.userprofile)
        if form.is_valid():
            form = form.save(commit=False)
            form.user.userprofile.points = 10000000000
            form.user.userprofile.paid = True
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profileview')

    return redirect('profileview')
