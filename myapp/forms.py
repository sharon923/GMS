import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from django import forms
from .models import packages

class SignupForm(forms.Form):
    
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'},),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),label='')
    fname = forms.CharField(required=True,  widget=forms.TextInput(attrs={'placeholder': 'Full Name'},),label='')
    lname = forms.CharField(required=True,  widget=forms.TextInput(attrs={'placeholder': 'Last Name'},),label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'email',
            'password',
            'confirm_password',
            'fname',
            'lname',

            Submit('submit', 'Submit', css_class='btn-success')
        )

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('The two password fields must match')
        return cleaned_data
