from django.contrib import admin

from users_info.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address_text",)
    # pass
    # list_filter = ('code',)
# Register your models here.
