from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Owner(models.Model):
    class ContactState(models.TextChoices):
        UNCONTACT = 'UC', _('Uncontacted')
        SENT_MAIL = 'SM', _('SentMail')
        SENT_WHATSAPP = 'SW', _('SentWhatsApp')
        NOT_INTERESTED = 'NI', _('NotInterested')
        INTERESTED = 'IR', _('Interested')

    national_id = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=30)
    mail = models.EmailField(max_length=30, blank=True, null=True, default='...')
    phone = models.CharField(max_length=20, blank=True, null=True, default='...')
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    contact_state = models.CharField( max_length=2, choices=ContactState.choices, default=ContactState.UNCONTACT,)

    def __str__(self):
        return '<Id: {} City: {} Mail: {} Phone: {}>' \
            .format(self.national_id, self.city, self.mail if self.mail is not None else '---',
                    self.phone if self.phone is not None else '---')
    

    def is_phone_valid(self):
        return len(self.phone)>=9
    
    def is_mail_valid( self ):
        from django.core.exceptions import ValidationError
        from django.core.validators import validate_email
        try:
            validate_email( self.mail )
            return True
        except ValidationError:
            return False
        
    def is_contact_data_valid(self):
        return self.is_phone_valid() and self.is_mail_valid()
    

    def is_no_valid_data(self):
        return not self.is_phone_valid() and not self.is_mail_valid()


class OwnerProfile(models.Model):
    person = models.OneToOneField(Owner, on_delete=models.CASCADE, related_name="profile")
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
    person = models.OneToOneField(Owner, on_delete=models.CASCADE, related_name="economic_profile")
    credit_cards = models.IntegerField()
    credit_balance = models.IntegerField()
    average_credit_balance = models.IntegerField()
    credit_card_balance = models.IntegerField()

    def __str__(self):
        return '<Id: {} CreditCards: {} Balance: {} Average: {} CC_Balance: {}>' \
            .format(self.person.national_id, self.credit_cards, self.credit_balance, self.average_credit_balance,
                    self.credit_card_balance)


class Car(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="cars")
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField(blank=True, null=True, default=0)
    plate = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return '<Id: {} Model: {} Year: {} Plate: {} Color: {}>' \
            .format(self.owner.national_id, self.model, self.year, self.plate, self.color)


class Operation(models.Model):
    operator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
