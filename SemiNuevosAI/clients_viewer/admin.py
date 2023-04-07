from django.contrib import admin

from .models import *

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("city", "national_id", "car_list")
    list_filter = ("city", )
    # search_fields = ("national_id__startswith", )
    search_fields = ("car_list", )
    class Meta:
        ordering = ("city")


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    pass

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "plate", "owner","color", "view_owner_link")
    class Meta:
        ordering = ("model", "year")


# admin.site.register(Owner)
# admin.site.register(Mail)
# admin.site.register(Phone)
# admin.site.register(Car)

