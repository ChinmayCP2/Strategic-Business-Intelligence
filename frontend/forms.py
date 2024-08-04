from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from lgd.models import StateModel, DistrictModel, SubDistrictModel, VillageModel
from strategicbi.models import CatagoryModel, DataModel

fields = ['name']
SORTING_CHOICES = tuple((field, field) for field in fields)

class LocationForm(forms.Form):
    
    '''Select location form'''
    state = forms.ModelChoiceField(
        queryset=StateModel.objects.all(), required=True, # pylint: disable=maybe-no-member
        widget=forms.Select(attrs={
            "class": "form-select","id": "id_state",
            "hx-get": "/load-districts/?state={{ value }}",
            "hx-target": "#id_district",
        })
    )
    district = forms.ModelChoiceField(
        queryset=DistrictModel.objects.none(),required=False, # pylint: disable=maybe-no-member
        initial=None,
        widget=forms.Select(attrs={
            "class": "form-select","id": "id_district",
            "hx-get": "/load-subdistricts/?district={{ value }}",
            "hx-target": "#id_subdistrict",
        })
    )
    subdistrict = forms.ModelChoiceField(
        queryset=SubDistrictModel.objects.none(),required=False, # pylint: disable=maybe-no-member
        initial=None,
        widget=forms.Select(attrs={
            "class": "form-select", "id": "id_subdistrict",
            "hx-get": "/load-villages/?subdistrict={{ value }}",
            "hx-target": "#id_village",
        })
    )
    village = forms.ModelChoiceField(
        queryset=VillageModel.objects.none(), # pylint: disable=maybe-no-member
        initial=None,
        required=False,
        widget=forms.Select(attrs={
            "class": "form-select", "id": "id_village"
        })
    )
    catagory = forms.ModelChoiceField(
        queryset=CatagoryModel.objects.all(), # pylint: disable=maybe-no-member
        empty_label="",
        widget=forms.Select(attrs={
            "class": "form-select", "id": "id_catagory"
        })
    )
    sorting = forms.ChoiceField(
        choices=SORTING_CHOICES,
        required=False,
        widget=forms.Select(attrs={ 
            "class": "form-select", "id": "id_sorting"
        })
    )
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username' , 'email', 'password1', 'password2']