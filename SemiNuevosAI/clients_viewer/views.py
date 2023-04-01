# Create your views here.
import json
import os
import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
    

def data_cleaner(request, option):
    file = 'E:\MyProjects\Django SemiNuevosAI\SemiNuevosAI\clients_viewer\static\data\data_clean.csv'
    os.system('clear')
    with open(file, 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        print(reader.fieldnames)
        owners = []
        total_contacts = 0
        complete_info_contacts = 0
        invalid_mail_count = 0
        invalid_phone_count = 0
        invalid_contact_count = 0
        national_id_list=[]
        owner_list = []
        phone_numbers_list = []
        mails_list=[]

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

            print(f'{national_id} {city} {mail} {phone}')
            
            owner = TempOwner(national_id = national_id, city = city)
            try:
                owner.save()
            except:
                print("oh owner")
            

            owner_phone = Phone(owner = owner, number = phone)
            try:
                owner_phone.save()
            except:
                print("oh phone", phone)


            owner_mail = Mail(owner = owner, mail = mail)
            try:
                owner_mail.save()
            except:
                print("oh mail", mail)

            append_owner(owner_list, owner)

            
  
            total_contacts +=1
            # if check_no_contact_info(mail, phone):
            #     invalid_contact_count += 1
            #     # print(f'1. mail: {mail} - phone: {phone}')
            # # elif not check_valid_phone(phone):
            # #     invalid_phone_count +=1
            # #     national_id_list.append(national_id) 
            # #     # print(f'2. mail: {mail} - phone: {phone}')
            # elif not check_valid_mail(mail):
            #     invalid_mail_count +=1
            #     national_id_list.append(national_id) 
            #     # print(f'3. mail: {mail} - phone: {phone}')
            # else:
            #     complete_info_contacts+=1
            #     # print(f'4. mail: {mail} - phone: {phone}')


        # print(len(national_id_list))
        # national_id_list = list(dict.fromkeys(national_id_list))
        # print(len(national_id_list))
        print_owner_list(owner_list)

        return JsonResponse({"msg": "OK", "total_contacts": total_contacts, "complete_info":complete_info_contacts,"invalid_mail":invalid_mail_count, "invalid_phone":invalid_phone_count, "invalid_contact":invalid_contact_count})

        global repeated_owner_cnt
        repeated_owner_cnt +=1            

def append_owner(owner_list, new_owner):
    repeated_owner_cnt = 0
    for owner in owner_list:
        if owner.national_id == new_owner.national_id:
            # if owner.phone != new_owner.phone:
            #     if not check_valid_phone(owner.phone):
            #         print('fill', new_owner.phone, owner.phone)
            #     else:
            #         print('update', new_owner.phone, owner.phone)
            #     owner.phone = new_owner.phone
            # if owner.mail != new_owner.mail:
            #     # if not check_valid_phone(owner.phone):
            #     #     print('fill', new_owner.phone, owner.phone)
            #     # else:
            #     print('update', new_owner.mail, owner.mail)
            repeated_owner_cnt += 1
    if repeated_owner_cnt == 0:
        owner_list.append(new_owner)

    
def print_owner_list(owner_list):
    print('Owner List Report')
    print(len(owner_list))
    
def check_valid_mail(mail):
    if not '@' in mail:
        return False
    return True

def check_valid_phone(phone):
    valid_num = re.findall('[0-9]+', phone)
    if not valid_num:
        return False
    if valid_num and len(valid_num[0]) != 9:
        return False
    return True

def check_no_contact_info(mail, phone):
    return not check_valid_mail(mail) and not check_valid_phone(phone)



            #     if not Owner.objects.filter(national_id=row['Cedula']).exists():
        #         owner.save()
        #         profile = OwnerProfile(person=owner,
        #                                age=row['Edad'],
        #                                education_level=row['Estudios'],
        #                                living_place_type=row['Tipo_Vivienda'],
        #                                real_state_units=row['Bienes'],
        #                                dependents=row['Cargas'])
        #         profile.save()

        #         economic_profile = EconomicProfile(person=owner,
        #                                            credit_cards=row['Tarjetas'],
        #                                            credit_balance=row['Saldo_Credito'],
        #                                            average_credit_balance=row['Saldo_Promedio'],
        #                                            credit_card_balance=row['Saldo_Tarjeta_Credito'])
        #         economic_profile.save()
        #     else:
        #         owner = Owner.objects.get(national_id=row['Cedula'])

        #     try:
        #         car = Car(owner=owner,
        #                   brand=row['Marca'],
        #                   model=row['Modelo'],
        #                   year=row['Año'],
        #                   plate=row['Placa'],
        #                   color=row['Color'])
        #         car.save()
        #     except:
        #         print(row)