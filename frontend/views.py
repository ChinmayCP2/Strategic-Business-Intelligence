from django.shortcuts import render
from lgd.models import DistrictModel, SubDistrictModel, VillageModel
from .forms import LocationForm
from strategicbi.models import DataModel
# Create your views here.

def index(request):
    '''index'''
    if request.method == 'POST':
        form = LocationForm(request.POST)
        
        data = request.POST
        stateCode = data.get('stateCode')
        district = data.get('district')
        subdistrict = data.get('subdistrict')
        village = data.get('village')
        datamodel_objects = DataModel.objects.all() # pylint: disable=maybe-no-member
        if stateCode:
            datamodel_objects = datamodel_objects.filter(stateCode=stateCode).values('id','name')
        if district:
            datamodel_objects = datamodel_objects.filter(districtCode=district).values('name')
        if subdistrict:
            datamodel_objects = datamodel_objects.filter(subdistrictCode=subdistrict).values('name')
        if village:
            datamodel_objects = datamodel_objects.filter(villageCode=village).values('name')
        print(datamodel_objects)
        context = {'form': form, 'data': datamodel_objects}
        return render(request, 'index.html', context)
            
    form = LocationForm()
    context = {'form': form}
    return render(request, 'index.html', context)

def load_districts(request):
    '''dropdown district'''
    stateCode = request.GET.get('stateCode')
    districts = DistrictModel.objects.filter(stateCode = stateCode) # pylint: disable=maybe-no-member
    # print(districts)
    context = {'districts' : districts}
    return render(request, 'district_options.html', context)

def load_subdistricts(request):
    '''dropdown of subdistrict'''
    district_code = request.GET.get('district')
    # print(district_code)
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    # print(state)
    subdistricts = SubDistrictModel.objects.filter(districtCode = district_code)# pylint: disable=maybe-no-member
    # print(subdistricts)
    context = {'subdistricts' : subdistricts}
    return render(request, 'subdistrict_options.html', context)

def load_villages(request):
    '''dropdown of subdistrict'''
    subdistrict_code = request.GET.get('subdistrict')
    print(subdistrict_code)
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    # print(state)
    villages = VillageModel.objects.filter(subdistrictCode = subdistrict_code)# pylint: disable=maybe-no-member
    # print(villages)
    context = {'villages' : villages}
    return render(request, 'village_options.html', context)

