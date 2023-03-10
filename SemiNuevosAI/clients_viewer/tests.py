from django.test import TestCase

from .models import Owner


class ClientsViewer(TestCase):
    owner1 = None

    def setUp(self):
        owner1 = Owner(national_id='1719874354', city = "Quito")
        owner1.save()
        # self.user1 = User(username="daniel", email="daniel@test.com", password="test")
        # self.user1.save()
        # self.user2 = User(username="chiki", email="chiki@test.com", password="test")
        # self.user2.save()
        # self.user3 = User(username="joha", email="joha@test.com", password="test")
        # self.user3.save()

    def test_count_number_of_users(self):
        owners = Owner.objects.all()
        self.assertEquals(1, len(owners))
