from django.contrib import admin
from apps.accounts.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('index_number',)
    list_filter = ('groups',)
    search_fields = ['index_number']

admin.site.register(Account, AccountAdmin)
