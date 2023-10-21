from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Account

@admin.register(Account)

class AccountAdmin(UserAdmin):

    list_display = ('email' , 'firstname' , 'lastname' , 'username', 'created_date', 'last_login', 'is_active')
    list_display_links = ('email' , 'firstname' , 'lastname' , 'username')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

