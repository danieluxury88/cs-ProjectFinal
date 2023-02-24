# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from .database_handler import *
from .file_reader import *

def index(request):

    owners = get_all_owners()
    a_owner = get_all_owners().first()
    a_cars = get_owner_cars(a_owner)


    profile = get_owner_profile(a_owner)
    e_profile = get_owner_economic_profile(a_owner)

    b_owners = get_all_owners_according_model('LUV DMAX 4X4')
    c_owners = get_all_owners_on_a_city('Quito')

    context = {'owners': c_owners,
               'profile': profile,
               'eprofile': e_profile,
               'cars': a_cars}
    return render(request, "clients_viewer/index.html", context)


def load_csv (request):
    import_csv("data_clean.csv")
    return HttpResponse("loaded ok")

# # Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})
