import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from django import forms
from ..models import packages
from django.forms import DateTimeInput


class UserProfileForm(forms.Form):
    def __init__(self, user_obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['addr'] = forms.CharField(required=True, label='',initial=user_obj.get('addr'), widget=forms.TextInput(attrs={'placeholder': 'address'},))
        self.fields['place'] = forms.CharField(required=True,label='', initial=user_obj.get('place'), widget=forms.TextInput(attrs={'placeholder': 'place'},))
        self.fields['pin_code'] = forms.CharField(required=True,label='', initial=user_obj.get('pincode'), widget=forms.TextInput(attrs={'placeholder': 'pincode'},))
        self.fields['phone'] = forms.CharField(required=True,label='', initial=user_obj.get('phone'), widget=forms.TextInput(attrs={'placeholder': 'contact no'}))

        package_options = ()
        for pack in packages.objects.all():
            if pack.pack_name == 'NO_PLAN':
                user_readable = (pack.pack_name, str(pack.pack_duration) + " Month plan" +  ", Rs: " + str(pack.pack_price) + ", " + str(pack.day_pickup) + " times pickup")
                package_options = (package_options) + (user_readable,)

        for pack in packages.objects.all():
            if pack.pack_name != 'NO_PLAN':
                user_readable = (pack.pack_name, str(pack.pack_duration) + " Month plan" +  ", Rs: " + str(pack.pack_price) + ", " + str(pack.day_pickup) + " times pickup")
                package_options = (package_options) + (user_readable,)
    
        self.fields['pack'] = forms.ChoiceField(choices=package_options, label='', initial=user_obj.get('pack'))
        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'addr',
            'place',
            'pin_code',
            'phone',
            'pack',
            Submit('submit', 'Update', css_class='btn-success')
        )

    def clean_pin_code(self):
        cleaned_data = super(UserProfileForm, self).clean()
        pin_code = self.cleaned_data.get('pin_code')
        if len(pin_code) != 6:
            raise forms.ValidationError('Pin code must be 6 digits long.')
        return cleaned_data

    def clean_phone(self):
        
        cleaned_data = super(UserProfileForm, self).clean()
        phone = self.cleaned_data.get('phone')
        if len(phone) != 10:
            raise forms.ValidationError('Phone number must be 10 digits long.')
        return cleaned_data

    def clean(self):
        
        cleaned_data = super().clean()
        return cleaned_data

class ScheduleForm(forms.Form):
    
    pick_date = forms.DateField(input_formats=['%d/%m/%Y', '%d-%m-%Y'] ,required=True, widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'},),label='')
    pick_time = forms.TimeField(required=True,  widget=forms.TextInput(attrs={'placeholder': '24 Hour time format'},),label='')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'pick_date',
            'pick_time',
            
            Submit('submit', 'Schedule', css_class='btn-success')
        )
