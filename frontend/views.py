from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from lgd.models import DistrictModel, SubDistrictModel, VillageModel, StateModel
from .forms import LocationForm, RegistrationForm
from strategicbi.models import DataModel

# Create your views here.

@login_required(login_url='/login')
def home(request):
    '''index'''
    form = LocationForm(request.POST or None)  
    context = {} 
    if request.method == 'POST':      
        data = request.POST
        state = data.get('state')
        district = data.get('district')
        subdistrict = data.get('subdistrict')
        village = data.get('village')
        catagory = data.get('catagory')
        sorting = data.get('sorting')
        # print(state, village, subdistrict, district)
        if village:
            pass
        if subdistrict:
            pass
        if district:
            try:
                fields = [field.name for field in DataModel._meta.get_fields()]  # pylint: disable=maybe-no-member
                state_instance = StateModel.objects.filter(pk=state).first() # pylint: disable=maybe-no-member
                district_instance = DistrictModel.objects.filter(pk=district,stateCode=state_instance).values('districtCode').first() # pylint: disable=maybe-no-member
                
                if not district_instance:
                    context = {'message': 'District not found'}
                else:
                    state_code = state_instance.get('stateCode')
                    district_code = district_instance.get('districtCode')

                    if sorting and sorting in fields and catagory:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code, # pylint: disable=maybe-no-member
                                                           catagory=catagory).order_by(sorting).values("name") 
                    elif catagory:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code, # pylint: disable=maybe-no-member
                                                           catagory=catagory).values("name") 
                    else:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code).values("name") # pylint: disable=maybe-no-member
                    context = {'places': places}
            except Exception as e:
                context = {'message': 'An error occurred: {}'.format(str(e))}
        if state:
            try:
                fields = [field.name for field in DataModel._meta.get_fields()]  # pylint: disable=maybe-no-member
                state_instance = StateModel.objects.filter(pk=state).values('stateCode').first() # pylint: disable=maybe-no-member
                print(state_instance.get('stateCode'))
                
                if not state_instance:
                    context = {'message': 'State not found'}
                else:
                    state_code = state_instance.get('stateCode')

                    if sorting and sorting in fields and catagory:
                        places = DataModel.objects.filter(stateCode=state_code, # pylint: disable=maybe-no-member
                                                           catagory=catagory).order_by(sorting).values("name") 
                    elif catagory:
                        places = DataModel.objects.filter(stateCode=state_code,  # pylint: disable=maybe-no-member
                                                           catagory=catagory).values("name") 
                    else:
                        places = DataModel.objects.filter(stateCode=state_code).values("name") # pylint: disable=maybe-no-member
                    context = {'places': places}
            except Exception as e:
                context = {'message': 'An error occurred: {}'.format(str(e))}    
    context['form'] = form
    return render(request, 'frontend/home.html', context)
    
    #     if state:
    #         try:
    #             fields = [field.name for field in DataModel._meta.get_fields()]  # pylint: disable=maybe-no-member
    #             state_instance = StateModel.objects.filter(pk=state).values('stateCode').first() # pylint: disable=maybe-no-member

    #             if not state_instance:
    #                 context = {'message': 'State not found'}
    #             else:
    #                 state_code = state_instance.get('stateCode')

    #                 if sorting and sorting in fields and catagory:
    #                     places = DataModel.objects.filter(stateCode=state_code, catagory=catagory).order_by(sorting).values("name")
    #                 elif catagory:
    #                     places = DataModel.objects.filter(stateCode=state_code, catagory=catagory).values("name")
    #                 else:
    #                     places = DataModel.objects.filter(stateCode=state_code).values("name")

    #                 context = {'places': places}

    #         except Exception as e:
    #             context = {'message': 'An error occurred: {}'.format(str(e))}

    # else:
    #     context = {'message': 'State not entered'}
    #     context['form'] = form
    # return render(request, 'frontend/home.html', context)

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form =  RegistrationForm()
    return render(request, "registration/signup.html", {"form" : form})


def load_districts(request):
    '''dropdown district'''
    state = request.GET.get('state')
    districts = DistrictModel.objects.filter(stateCode = state) # pylint: disable=maybe-no-member
    # print(districts)
    context = {'districts' : districts}
    return render(request, 'dropdown_options/district_options.html', context)

def load_subdistricts(request):
    '''dropdown of subdistrict'''
    district_code = request.GET.get('district')
    # print(district_code)
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    # print(state)
    subdistricts = SubDistrictModel.objects.filter(districtCode = district_code)# pylint: disable=maybe-no-member
    # print(subdistricts)
    context = {'subdistricts' : subdistricts}
    return render(request, 'dropdown_options/subdistrict_options.html', context)

def load_villages(request):
    '''dropdown of subdistrict'''
    subdistrict_code = request.GET.get('subdistrict')
    print(subdistrict_code)
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    # print(state)
    villages = VillageModel.objects.filter(subdistrictCode = subdistrict_code)# pylint: disable=maybe-no-member
    # print(villages)
    context = {'villages' : villages}
    return render(request, 'dropdown_options/village_options.html', context)

