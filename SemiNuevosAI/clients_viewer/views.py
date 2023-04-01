# Create your views here.
import json
import os
import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .database_handler import *
from .file_reader import *
from .models import Owner, TempOwner

repeated_owner_cnt = 0




def test(request):
    return render(request, "clients_viewer/test.html")

def owners_list(request):
    owners = Owner.objects.all().order_by('city')
    context = {'owners': owners}
    return render(request, "clients_viewer/new_test.html", context)

def owners_by_city(request, city):
    owners = Owner.objects.filter(city__icontains=city)
    context = {'owners': owners}
    return render(request, "clients_viewer/new_test.html", context)

def owners_by_model(request, model):
    owners = Owner.objects.filter(cars__model__icontains =model).order_by('city')
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


def load_csv (request):
    # import_csv("data_clean.csv")
    import_csv('E:\MyProjects\Django SemiNuevosAI\SemiNuevosAI\clients_viewer\static\data\data_clean.csv')
    return HttpResponse("loaded ok")


def profile(request, profile_id):
    owner = Owner.objects.get(id=profile_id)
    profile = get_owner_profile(owner)
    eprofile = get_owner_economic_profile(owner)
    cars = get_owner_cars(owner)
    operations = Operation.objects.filter(owner =owner).order_by('-date')
    print("Operations" , operations)
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

        operation = Operation(operator = requester, owner = owner, comment = content )
        operation.save()

        return JsonResponse({"msg": "OK", "comment": content})
    

from django.conf import settings

def data_cleaner(request, option):
    if option == 0:
        TempOwner.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM clients_viewer_tempowner;")
            cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='clients_viewer_tempowner';")

        Mail.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM clients_viewer_mail;")
            cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='clients_viewer_mail';")
        
        Phone.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM clients_viewer_phone;")
            cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='clients_viewer_phone';")

        return JsonResponse({"status":"ok"})
    else:
        file = settings.BASE_DIR / 'data/data_clean.csv'
        os.system('clear')
        with open(file, 'r', encoding="utf8") as file:
            reader = csv.DictReader(file)
            print(reader.fieldnames)
            total_contacts = 0


            for row in reader:
                # Check if email already exists in database
                national_id=row['Cedula']
                national_id = re.sub(r"\s+", "", national_id)
                
                city=row['Ciudad']
                city = re.sub(r"\s+", "", city)

                mail=row['Mail']
                mail = ''.join(mail.split())

                phone=row['Telefono']
                phone = ''.join(phone.split())

                if len(phone) < 9:
                    print(phone, type(phone), len(phone))

                # print(f'{total_contacts}: {national_id} {city} {mail} {phone}')
                
                owner = TempOwner(national_id = national_id, city = city)
                try:
                    owner.save()
                except (ValueError, IntegrityError) as e:
                    owner = TempOwner.objects.get(national_id = national_id)
                

                owner_phone = Phone(owner = owner, number = phone)
                try :
                    owner_phone.save()
                # except (ValueError, IntegrityError) as e:
                #     print('Error:', str(e), phone)
                except ValidationError:
                    print('validation error')


                owner_mail = Mail(owner = owner, mail = mail)
                try:
                    owner_mail.save()
                except (ValueError, IntegrityError) as e:
                    print('Error:', str(e), mail)

                
    
                total_contacts +=1

            # return JsonResponse({"msg": "OK", "total_contacts": total_contacts, "complete_info":complete_info_contacts,"invalid_mail":invalid_mail_count, "invalid_phone":invalid_phone_count, "invalid_contact":invalid_contact_count})
            return JsonResponse({"msg":"ok"})

        global repeated_owner_cnt
        repeated_owner_cnt +=1            

