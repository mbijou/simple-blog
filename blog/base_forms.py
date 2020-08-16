from django.forms import forms
from django.forms import FileField, BooleanField


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if isinstance(field, FileField) or isinstance(field, BooleanField):
                continue
            field.widget.attrs['class'] = 'form-control'
