import csv

from .models import *

def import_csv(file):
    with open(file, 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        print(reader.fieldnames)
        owners = []
        for row in reader:
            # Check if email already exists in database
            owner = Owner(
                national_id=row['Cedula'],
                city=row['Ciudad'],
                mail=row['Mail'],
                phone=row['Telefono'])
            if not Owner.objects.filter(national_id=row['Cedula']).exists():
                owner.save()
                profile = OwnerProfile(person=owner,
                                       age=row['Edad'],
                                       education_level=row['Estudios'],
                                       living_place_type=row['Tipo_Vivienda'],
                                       real_state_units=row['Bienes'],
                                       dependents=row['Cargas'])
                profile.save()

                economic_profile = EconomicProfile(person=owner,
                                                   credit_cards=row['Tarjetas'],
                                                   credit_balance=row['Saldo_Credito'],
                                                   average_credit_balance=row['Saldo_Promedio'],
                                                   credit_card_balance=row['Saldo_Tarjeta_Credito'])
                economic_profile.save()
            else:
                owner = Owner.objects.get(national_id=row['Cedula'])

            try:
                car = Car(owner=owner,
                          brand=row['Marca'],
                          model=row['Modelo'],
                          year=row['Año'],
                          plate=row['Placa'],
                          color=row['Color'])
                car.save()
            except:
                print(row)