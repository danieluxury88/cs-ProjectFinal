# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json

from .database_handler import *
from .file_reader import *


def test(request):
    return render(request, "clients_viewer/test.html")


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