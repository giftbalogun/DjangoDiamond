from django.contrib import admin
from accountprofile.models import Package, Referral

# Register your models here.


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'is_published')

    list_display_links = ('id', 'title')

    list_editable = ('is_published',)

    list_per_page = 25


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'referree')

    list_display_links = ('id', 'user')

    list_per_page = 25
