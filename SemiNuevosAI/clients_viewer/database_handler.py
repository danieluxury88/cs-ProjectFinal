from .models import *


# get all objects
def get_all_owners():
    return Owner.objects.all()


def get_all_cars():
    return Car.objects.all()


# User profile

def get_owner_economic_profile(owner):
    return owner.economic_profile


def get_owner_profile(owner):
    return owner.profile


# Owners
def get_all_owners_on_a_city(city):
    return Owner.objects.filter(city=city)


# Vehicles

def get_owner_cars(owner):
    return owner.cars.all()


def get_all_owners_according_model(model):
    return Owner.objects.filter(cars__model=model)


