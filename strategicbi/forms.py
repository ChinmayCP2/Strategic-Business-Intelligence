from django import forms

from lgd.models import StateModel, DistrictModel
from strategicbi.models import CatagoryModel

fields = ['name']
SORTING_CHOICES = tuple((field, field) for field in fields)
class StateForm(forms.Form):
    '''sort by state form'''
    state = forms.ModelChoiceField(queryset=StateModel.objects.all(), # pylint: disable=maybe-no-member
                                    empty_label="All",  # Add this to display "All" as the first option
                                    required=False,
                                    widget=forms.Select(attrs={
                                    "class": "form-select","id": "id_state"})) # pylint: disable=maybe-no-member

# class LocationForm(forms.Form):
#     '''Select location form'''
#     state = forms.ModelChoiceField(
#         queryset=StateModel.objects.all(), # pylint: disable=maybe-no-member
#         widget=forms.Select(attrs={
#             "class": "form-select w-50","id": "id_state",
#             "hx-get": "load-districts/?state={{ value }}",
#             "hx-target": "#id_district",
#         })
#     )
#     district = forms.ModelChoiceField(
#         queryset=DistrictModel.objects.none(), # pylint: disable=maybe-no-member
#         initial=None,
#         widget=forms.Select(attrs={
#             "class": "form-select w-50","id": "id_district",
#         })
#     )
#     catagory = forms.ModelChoiceField(
#         queryset=CatagoryModel.objects.all().distinct('catagory'), # pylint: disable=maybe-no-member
#         initial= CatagoryModel.objects.get(catagory="all"),
#         widget=forms.Select(attrs={
#             "class": "form-select w-50", "id": "id_catagory"
#         })
#     )
    
class LocationForm(forms.Form):
    '''Select location form'''
    state = forms.ModelChoiceField(
        queryset=StateModel.objects.all(), 
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_state",
            "hx-get": "load-districts/?state={{ value }}",
            "hx-target": "#id_district",
            "data-placeholder": "Select a state"
        }),
    )
    district = forms.ModelChoiceField(
        queryset=DistrictModel.objects.none(), 
        initial=None,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_district",
        })
    )
    catagory = forms.ModelChoiceField(
        queryset=CatagoryModel.objects.all().distinct('catagory'), 
        initial= CatagoryModel.objects.get(catagory="all"),
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_catagory",
        })
    )
