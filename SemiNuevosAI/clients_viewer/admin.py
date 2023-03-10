from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Operation)
admin.site.register(Owner)
admin.site.register(OwnerProfile)
admin.site.register(EconomicProfile)
admin.site.register(Car)

