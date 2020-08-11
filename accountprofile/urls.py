from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from accountprofile.views import IndexView, DashboardView, edit_profile, AccountView, PackageListView, make_payment, check_payment  # , packageupdate
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('dashboard',
         login_required(DashboardView.as_view()), name="dashboard"),
    path('profile',
         login_required(AccountView.as_view()), name="profileview"),
    path('package',
         login_required(PackageListView.as_view()), name="package"),
    path('update', edit_profile, name='edit_profile'),

    path('payment/<int:id>', make_payment, name="payment"),

    path('paid/', check_payment, name="paid"),

    #path('packageupdate', packageupdate, name='packageupdate'),

]
