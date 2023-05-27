import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from django import forms
from ..models import history, delivery_status

class PickupUpdateForm(forms.Form):
    def __init__(self, history_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_status = []
        for each_status in delivery_status.objects.all():
            all_status.append((str(history_id.id) + '##$$&&' + each_status.status, each_status.ui_text))
        
        intial_value = str(history_id.id) + '##$$&&' + history_id.choice.status
        self.fields['status'] = forms.ChoiceField(choices=all_status, label='', initial=intial_value, 
                                                  widget=forms.Select(attrs={'onchange': 'submit();'}))
        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'status'
        )
