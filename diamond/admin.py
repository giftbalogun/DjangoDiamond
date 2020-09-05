from django.contrib import admin
from diamond.models import UserProfile

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bankname', 'package',
                    'is_published')

    list_display_links = ('id', 'user')

    list_editable = ('is_published',)

    list_per_page = 25
