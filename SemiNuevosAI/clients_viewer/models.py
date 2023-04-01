from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator




class User(AbstractUser):
    pass


class Owner(models.Model):
    national_id = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=30)
    mail = models.EmailField(max_length=30, blank=True, null=True, default='...')
    phone = models.CharField(max_length=20, blank=True, null=True, default='...')
    name = models.CharField(max_length=50, blank=True, null=True, default='')

    def __str__(self):
        return '<Id: {} City: {} Mail: {} Phone: {}>' \
            .format(self.national_id, self.city, self.mail if self.mail is not None else '---',
                    self.phone if self.phone is not None else '---')


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


class TempOwner(models.Model):
    # national_id = models.CharField(max_length=10)
    national_id = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=30)
    name = models.CharField(max_length=50, blank=True, null=True, default='')


def validate_phone(value):
    print(value)
    # if not value.isdigit() or len(value) < 9:
    if len(value) < 9:
        print('error ', value)
        raise ValidationError("Phone number must have at least 9 digits.")
    


    
class Phone(models.Model):
    owner = models.ForeignKey(TempOwner, on_delete=models.CASCADE, related_name='phones')
    number = models.CharField(max_length=20, validators=[MinLengthValidator(9)])

    # class Meta:
    #     unique_together = ('owner', 'number')

    def __str__(self) -> str:
        real_len = len(self.number)
        return f'{self.owner.national_id} {self.number} {real_len}'



def validate_email(value):
    if value.count('@') != 1:
        print("test")
        raise ValidationError('Email address must contain exactly one "@" symbol.')

class Mail(models.Model):
    owner = models.ForeignKey(TempOwner, on_delete=models.CASCADE, related_name='mails')
    mail = models.EmailField(max_length=30, blank=True, null=True, default='...', validators=[validate_email])
    # mail = models.EmailField(max_length=30, blank=True, null=True, default='...')
    
    # class Meta:
    #     unique_together = ('owner', 'mail')

    def __str__(self) -> str:
        return f'{self.owner.national_id} {self.mail}'