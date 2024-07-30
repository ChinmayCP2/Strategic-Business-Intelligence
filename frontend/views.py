from django.shortcuts import render
from lgd.models import DistrictModel, SubDistrictModel, VillageModel
from .forms import LocationForm
# Create your views here.
def index(request):
    form = LocationForm()
    context = {'form' : form}
    return render(request, 'index.html', context)

def load_districts(request):
    '''dropdown district'''
    stateCode = request.GET.get('stateCode')
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    print(stateCode)
    districts = DistrictModel.objects.filter(stateCode = stateCode)# pylint: disable=maybe-no-member
    print(districts)
    context = {'districts' : districts}
    return render(request, 'district_options.html', context)

def load_subdistricts(request):
    '''dropdown of subdistrict'''
    district_code = request.GET.get('district')
    print(district_code)
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    # print(state)
    subdistricts = SubDistrictModel.objects.filter(districtCode = district_code)# pylint: disable=maybe-no-member
    print(subdistricts)
    context = {'subdistricts' : subdistricts}
    return render(request, 'subdistrict_options.html', context)

def load_villages(request):
    '''dropdown of subdistrict'''
    subdistrict_code = request.GET.get('subdistrict')
    print(subdistrict_code)
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    # print(state)
    villages = VillageModel.objects.filter(subdistrictCode = subdistrict_code)# pylint: disable=maybe-no-member
    print(villages)
    context = {'villages' : villages}
    return render(request, 'village_options.html', context)