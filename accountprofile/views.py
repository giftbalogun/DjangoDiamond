from python_paystack.objects.transactions import Transaction
from python_paystack.managers import TransactionsManager
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from allauth.account.forms import ChangePasswordForm
from django.views.generic.edit import FormView
from accountprofile.forms import UserUpdateForm, ProfileUpdateForm, PackageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import UpdateView
from django.contrib.auth.models import User
from diamond.models import UserProfile

from accountprofile.models import Package
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


class IndexView(TemplateView):
    template_name = "index.html"


class DashboardView(TemplateView):
    template_name = "profile/dashboard.html"


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

    '''
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        print(form.cleaned_data)
        form.package = form.cleaned_data['package']
        form.save()
        print(form.cleaned_data)
        return super().form_valid(form)
        '''


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

    transaction_manager = TransactionsManager()
    transaction = transaction_manager.initialize_transaction(
        'STANDARD', transaction)
    return redirect(transaction.authorization_url)


@csrf_exempt
# @require_http_methods(["POST"])
def check_payment(request):
    packageid = request.user.userprofile.package.id
    price = request.user.userprofile.package.price
    if request.method == "POST":
        response = json.loads(request.body)
        event = response["event"]
        status = response["data"]["status"]
        sent_email = response["data"]["customer"]["email"]
        plan = response["data"]["plan"]["name"]
        amount_paid = response["data"]["amount"]
        try:
            user = get_object_or_404(User, email=sent_email)
            if event == "charge.success" and status == "success":
                print("paid")
                user.userprofile.points = 10000000000
                if plan == packageid and amount_paid == price:
                    user.userprofile.plan = "BC"
                else:
                    user.userprofile.plan == "BB"
                user.userprofile.paid = True
                user.save()
        except:
            HttpResponse(status_code=400)
    return HttpResponse('success')


@csrf_exempt
@require_http_methods(["POST"])
def index(request):
    if request.method == "POST":
        response = json.loads(request.body)
        event = response["event"]
        status = response["data"]["status"]
        sent_email = response["data"]["customer"]["email"]
        plan = response["data"]["plan"]["name"]
        amount_paid = response["data"]["amount"]
        try:
            user = get_object_or_404(User, email=sent_email)
            if event == "charge.success" and status == "success":
                print("paid")
                user.userprofile.points = 10000000000
                if plan == "basic" and amount_paid == 70000:
                    user.userprofile.plan = "BC"
                else:
                    user.userprofile.plan == "BB"
                user.userprofile.paid = True
                user.save()
        except:
            HttpResponse(status_code=400)
    return HttpResponse('success')
