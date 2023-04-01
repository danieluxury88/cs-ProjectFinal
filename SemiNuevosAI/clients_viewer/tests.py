from django.test import TestCase

from .models import Owner,Car

import csv
import re
from collections import defaultdict
from django.db import transaction
from django.conf import settings
from django.db import IntegrityError


class ClientsViewer(TestCase):
    owner1 = None

    def setUp(self):
        self.owner1 = Owner(national_id='1719874354', city = "Quito")
        self.owner1.save()

    def test_count_number_of_users(self):
        owners = Owner.objects.all()
        self.assertEquals(1, len(owners))


    def test_no_repeated_cars(self):
        print(self.owner1)
        car1 = Car(owner=self.owner1, brand="Chevrolet", model="Aveo", year=2006, plate="pbu1212", color="")
        car1.save()
        car2 = Car(owner=self.owner1, brand="Chevrolet", model="Aveo", year=2006, plate="pbu1212", color="beige")
        car2.save()
        self.assertEquals(2, Car.objects.all().count())
