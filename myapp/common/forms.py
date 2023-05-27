import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from django import forms
from ..models import packages
import re


class LoginForm(forms.Form):
    uname = forms.CharField(required= True, widget=forms.TextInput(attrs={'placeholder': 'Email'},),label='')
    password = forms.CharField(required= True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),label='')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'uname',
            'password',
            Submit('signin', 'Sign in', css_class='btn-success'),
            HTML('<a class="btn btn-success" href={% url "signup" %}>Sign up</a>'),
        )
    
    def default_user_name(self,uname):
        self.fields['uname'].initial = uname

class SignupForm(forms.Form):
    
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'},),label='')
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

    def clean_password(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        if len(password) < 8:
             raise forms.ValidationError('Password must be at least 8 characters long.')
    
    # Add the regular expression pattern to match at least one special character
        special_char_pattern = r'[\W_]'
    
        if not re.search(special_char_pattern, password):
             raise forms.ValidationError('Password must contain at least one special character.')
    
        return password

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('The two password fields must match')
        return cleaned_data


    