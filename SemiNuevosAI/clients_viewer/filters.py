import django_filters
from django_filters import BooleanFilter

from .models import *

class OwnerFilter(django_filters.FilterSet):
    has_phone = BooleanFilter(field_name="phone")
    has_mail = BooleanFilter(field_name="mail")
    class Meta:
        model = Owner
        fields = '__all__'
        exclude = ['national_id', 'mail', 'phone', 'name']