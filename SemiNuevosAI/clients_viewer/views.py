# Create your views here.
import json
import os
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .database_handler import *
from .file_reader import *
from .models import Owner


def test(request):
    return JsonResponse({"msg": "OK"})


def report(request):
    owners = Owner.objects.all()

    # Phones
    owners_with_phone = Owner.objects.filter(
        Q(phones__isnull=False)).distinct()

    owners_with_no_phone = Owner.objects.annotate(
        num_phones=Count('phones')).filter(num_phones__lte=0)

    owners_with_multiple_phones = Owner.objects.annotate(
        num_phones=Count('phones')).filter(num_phones__gte=2)

    owners_with_phone_no_distinct = Owner.objects.filter(
        Q(phones__isnull=False))

    # Mails
    owners_with_mail = Owner.objects.filter(
        Q(mails_addrs__isnull=False)).distinct()

    owners_with_no_mail = Owner.objects.annotate(
        num_mails=Count('mails_addrs')).filter(num_mails__lte=0)

    owners_with_multiple_mails = Owner.objects.annotate(
        num_mails=Count('mails_addrs')).filter(num_mails__gte=2)

    owners_with_mail_no_distinct = Owner.objects.filter(
        Q(mails_addrs__isnull=False)).distinct()

    #Phone and Mail

    owners_with_no_phone_or_mail = Owner.objects.exclude(
        Q(phones__isnull=False) | Q(mails_addrs__isnull=False))

    owners_with_phone_and_mail = Owner.objects.filter(
        Q(phones__isnull=False) & Q(mails_addrs__isnull=False)).distinct()

    cities = Owner.objects.order_by('city').values_list(
        'city', flat=True).distinct()
    cities = list(cities)
    

    
    #Cars
    owners_with_one_car = Owner.objects.annotate(
        num_cars=Count('cars')).filter(num_cars=1)
    
    owners_with_multiple_cars = Owner.objects.annotate(
        num_cars=Count('cars')).filter(num_cars__gte=2)


    cars = Car.objects.all()
    models = Car.objects.order_by('model').values_list(
        'model', flat=True).distinct()
    models = list(models)


    return JsonResponse({"msg": "OK",
                         "owners": owners.count(),
                         "owners_with_no_phone_nor_mail": owners_with_no_phone_or_mail.count(),
                         "owners_with_phone": owners_with_phone.count(),
                         "owners_with_no_phone": owners_with_no_phone.count(),
                         "owners_with_multiple_phones": owners_with_multiple_phones.count(),
                         "owners_with_phone_no_distinct": owners_with_phone_no_distinct.count(),
                         "owners_with_mail": owners_with_mail.count(),
                         "owners_with_no_mail": owners_with_no_mail.count(),
                         "owners_with_multiple_mails": owners_with_multiple_mails.count(),
                         "owners_with_mail_no_distinct": owners_with_mail_no_distinct.count(),
                         "owners_with_phone_and_mail": owners_with_phone_and_mail.count(),
                         "owners_with_one_car": owners_with_one_car.count(),
                         "owners_with_multiple_cars": owners_with_multiple_cars.count(),

                         "cars": cars.count(),
                         "cities": cities,
                         "cities_count": len(cities),
                         "models": models,
                         "models_count": len(models),
                         })


def owners_list(request):
    owners = Owner.objects.all().order_by('city')
    context = {'owners': owners}
    return render(request, "clients_viewer/new_test.html", context)


def owners_by_city(request, city):
    owners = Owner.objects.filter(city__icontains=city)
    context = {'owners': owners}
    return render(request, "clients_viewer/new_test.html", context)


def owners_by_model(request, model):
    owners = Owner.objects.filter(
        cars__model__icontains=model).order_by('city')
    context = {'owners': owners}
    return render(request, "clients_viewer/new_test.html", context)


def index(request):
    owners = get_all_owners()
    a_owner = get_all_owners().first()
    a_cars = get_owner_cars(a_owner)

    profile = get_owner_profile(a_owner)
    e_profile = get_owner_economic_profile(a_owner)

    b_owners = get_all_owners_according_model('LUV DMAX 4X4')
    c_owners = get_all_owners_on_a_city('Ambato')

    context = {'owners': owners,
               'profile': profile,
               'eprofile': e_profile,
               'cars': a_cars}
    return render(request, "clients_viewer/index.html", context)


def profile(request, profile_id):
    owner = Owner.objects.get(id=profile_id)
    profile = get_owner_profile(owner)
    eprofile = get_owner_economic_profile(owner)
    cars = get_owner_cars(owner)
    operations = Operation.objects.filter(owner=owner).order_by('-date')
    print("Operations", operations)
    context = {'owner': owner,
               'profile': profile,
               'eprofile': eprofile,
               'cars': cars,
               'operations': operations}
    return render(request, "clients_viewer/profile.html", context)


@csrf_exempt
def register(request, profile_id):
    if request.method == "POST":
        print("handled")
        data = json.loads(request.body)
        owner = Owner.objects.get(id=profile_id)
        content = data["content"]
        requester = request.user

        operation = Operation(operator=requester, owner=owner, comment=content)
        operation.save()

        return JsonResponse({"msg": "OK", "comment": content})


def data_cleaner(request, option):
    if option == 0:
        Owner.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM clients_viewer_owner;")
            cursor.execute(
                "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='clients_viewer_owner';")

        Mail.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM clients_viewer_mail;")
            cursor.execute(
                "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='clients_viewer_mail';")

        Phone.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM clients_viewer_phone;")
            cursor.execute(
                "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='clients_viewer_phone';")

        Car.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM clients_viewer_car;")
            cursor.execute(
                "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='clients_viewer_car';")

        return JsonResponse({"status": "ok"})
    elif option == 1:
        file = settings.BASE_DIR / 'data/data_clean_owners.csv'
        os.system('clear')
        with open(file, 'r', encoding="utf8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Check if email already exists in database
                national_id = row['Id']
                national_id = re.sub(r"\s+", "", national_id)

                city = row['City']
                city = re.sub(r"\s+", "", city)

                mail = row['Mail']
                mail = ''.join(mail.split())

                phone = row['Phone']
                phone = ''.join(phone.split())

                owner = Owner(national_id=national_id, city=city)
                try:
                    owner.save()
                except (ValueError, IntegrityError) as e:
                    owner = Owner.objects.get(national_id=national_id)

                owner_phone = Phone(owner=owner, number=phone)
                try:
                    owner_phone.save()
                except ValidationError:
                    pass

                owner_mail = Mail(owner=owner, mail=mail)
                try:
                    owner_mail.save()
                except (ValueError, IntegrityError, ValidationError) as e:
                    pass

            return JsonResponse({"msg": "ok"})

    elif option == 2:
        input_file = settings.BASE_DIR / 'data/data_clean_cars.csv'
        output_file = settings.BASE_DIR / 'data/data_clean_cars_output.csv'
        os.system('clear')
        with open(input_file, 'r') as input_file, open(output_file, 'w', newline='') as output_file:
            # Create a CSV reader and writer objects
            reader = csv.DictReader(input_file)
            writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)

            # Write the header row to the output CSV file
            writer.writeheader()

            # Use a dictionary to keep track of which records we've already seen
            seen_records = {}

            # Loop over each row in the input CSV file
            for row in reader:
                # Check if we've already seen a record with this ID, model, and year
                key = (row['Id'], row['Model'].lower().replace(
                    '-', '').replace(' ', ''))
                if key in seen_records:
                    # We've already seen this record, so update it with missing information
                    if row['Year'] != 0:
                       seen_records[key]['Year'] = row['Year']
                    if row['Color']:
                        if not seen_records[key]['Color']:
                            seen_records[key]['Color'] = row['Color']
                    if row['Plate']:
                        # Check if the plate number is already in the record or a minor variation
                        plate_number = row['Plate'].replace("-", "")
                        if plate_number not in seen_records[key]['Plate'].replace("-", ""):
                            seen_records[key]['Plate'] = f"{seen_records[key]['Plate']} {row['Plate']}"
                    continue

                # This is a new record, so add it to the dictionary of seen records
                seen_records[key] = row

            for row in seen_records.values():
                 # Write the row to the output CSV file
                writer.writerow(row)
                owner = Owner.objects.get(national_id=row['Id'])
                car = Car(owner=owner, brand = row['Brand'], model = row['Model'], year = row['Year'], plate = row['Plate'], color = row['Color'] )
                car.save()


        return JsonResponse({"msg": "ok"})
