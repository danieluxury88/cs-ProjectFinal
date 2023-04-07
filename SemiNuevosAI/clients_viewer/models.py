from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html


class User(AbstractUser):
    pass


class Owner(models.Model):
    national_id = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=30)
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    
    def __str__(self) -> str:
        return f'{self.national_id} {self.city}'
    
    def car_list(self):
        return ", ".join([car.__str__() for car in self.cars.all()])
    car_list.short_description = "Cars Linked"


class Phone(models.Model):
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='phones')
    number = models.CharField(max_length=20, validators=[MinLengthValidator(9)])

    class Meta:
        unique_together = ('owner', 'number')

    def validate_phone(self):
        # if not value.isdigit() or len(value) < 9:
        if not self.number.isdigit() or len(self.number) < 9:
            raise ValidationError("Phone number must have at least 9 digits.")

    def full_clean(self, exclude=None, validate_unique=True):
        super().full_clean(exclude=exclude, validate_unique=validate_unique)
        self.validate_phone()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.owner.national_id} {self.number}'


class Mail(models.Model):
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='mails_addrs')
    mail = models.EmailField(max_length=30, blank=True,
                             null=True, default='...')

    class Meta:
        unique_together = ('owner', 'mail')

    def validate_email(self):
        if not self.mail or self.mail.count('@') != 1:
            raise ValidationError(
                'Email address must not be empty and contain exactly one "@" symbol.')

    def full_clean(self, exclude=None, validate_unique=True):
        super().full_clean(exclude=exclude, validate_unique=validate_unique)
        self.validate_email()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.owner.national_id} {self.mail}'
    

class Car(models.Model):
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name="cars")
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField(blank=True, null=True, default=0)
    plate = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)


    class Meta:
        unique_together = ('owner', 'brand','model', 'year', 'plate', 'color' )

    def __str__(self):
        return '< Model: {} Year: {} Plate: {} Color: {}>' \
            .format(self.model, self.year, self.plate, self.color)
    
    def view_owner_link(self):
        url = (
            reverse("admin:clients_viewer_owner_changelist")
            + "?"
            + urlencode({"owner__pk": f"{self.owner.pk}"})
        )
        return format_html('<a href="{}"> Owner</a>', url)


class OwnerProfile(models.Model):
    person = models.OneToOneField(
        Owner, on_delete=models.CASCADE, related_name="profile")
    age = models.IntegerField()
    education_level = models.CharField(max_length=30)
    living_place_type = models.CharField(max_length=30)
    real_state_units = models.IntegerField()
    dependents = models.IntegerField()

    def __str__(self):
        return '<Id: {} Age: {} Education: {} Residence: {}/{} Loads: {}>' \
            .format(self.person.national_id, self.age, self.education_level, self.living_place_type,
                    self.real_state_units, self.dependents)


class EconomicProfile(models.Model):
    person = models.OneToOneField(
        Owner, on_delete=models.CASCADE, related_name="economic_profile")
    credit_cards = models.IntegerField()
    credit_balance = models.IntegerField()
    average_credit_balance = models.IntegerField()
    credit_card_balance = models.IntegerField()

    def __str__(self):
        return '<Id: {} CreditCards: {} Balance: {} Average: {} CC_Balance: {}>' \
            .format(self.person.national_id, self.credit_cards, self.credit_balance, self.average_credit_balance,
                    self.credit_card_balance)




class Operation(models.Model):
    operator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
