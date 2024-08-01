from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from lgd.models import StateModel, DistrictModel, SubDistrictModel, VillageModel
from strategicbi.models import CatagoryModel, DataModel


class LocationForm(forms.Form):
    '''select location form'''
    # stateCode = forms.ModelChoiceField(queryset=StateModel.objects.all(),  # pylint: disable=maybe-no-member
    #                                 widget=forms.Select(attrs={"hx-get": "load-districts/","hx-target" : "#id_district", "hx-trigger": "change" }))
    state = forms.ModelChoiceField(queryset=StateModel.objects.all(), 
                                   required=True, to_field_name='stateCode',
                                   widget=forms.Select(attrs=
                                                       {"hx-get": "/load-districts/?state={{ value }}",
                                                             "hx-target" : "#id_district", 
                                                            } ))
    district = forms.ModelChoiceField(queryset=DistrictModel.objects.none(),
                                       to_field_name='districtCode' ,required=False,
                                       widget=forms.Select(attrs={"hx-get": "/load-subdistricts/?district={{ value }}", 
                                                             "hx-target" : "#id_subdistrict",
                                                            })) # pylint: disable=maybe-no-member
    subdistrict = forms.ModelChoiceField(queryset=SubDistrictModel.objects.none(),
                                          to_field_name='subdistrictCode' ,required=False,
                                         widget=forms.Select(attrs=
                                                             {"hx-get": "/load-villages/?subdistrict={{ value }}", 
                                                             "hx-target" : "#id_village", 
                                                            })) # pylint: disable=maybe-no-member
    village = forms.ModelChoiceField(queryset=VillageModel.objects.none(),to_field_name='villageCode', required=False) # pylint: disable=maybe-no-member
    catagory = forms.ModelChoiceField(queryset=CatagoryModel.objects.all(), required=False)
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username' , 'email', 'password1', 'password2']