from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from allauth.account.forms import ChangePasswordForm
from django.views.generic.edit import FormView
from accountprofile.forms import UserUpdateForm, ProfileUpdateForm, PackagesForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import UpdateView
from django.contrib.auth.models import User
from diamond.models import UserProfile

from accountprofile.models import Package


class IndexView(TemplateView):
    template_name = "index.html"


class DashboardView(TemplateView):
    template_name = "profile/dashboard.html"


class AccountView(TemplateView):
    template_name = "profile/profile.html"


class PackageListView(ListView):
    model = Package
    form_class = PackagesForm
    template_name = 'profile/package.html'
    context_object_name = 'queryset'
    queryset = Package.objects.order_by('price')

    def get_context_data(self, **kwargs):
        # package = .objects.order_by('-timestamp')
        form = self.form_class(self.request.POST)
        context = super().get_context_data(**kwargs)
        #context['popular'] = popular
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            package = form.cleaned_data['package']
            form = self.form_class()
            return HttpResponseRedirect('dashboard')

        return render(request, self.template_name, {'form': form})


@login_required
def edit_profile(request):
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
    }

    return render(request, 'profile/update.html', context)


@login_required
def packageupdate(request):
    if request.method == 'POST':
        package_form = PackageForm(request.POST,
                                   instance=request.user.userprofile)
        if package_form.is_valid():
            package_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('edit_profile')

    else:
        package_form = PackageForm(instance=request.user.userprofile)

    context = {
        'package_form': package_form
    }

    return render(request, 'profile/package.html', context)
