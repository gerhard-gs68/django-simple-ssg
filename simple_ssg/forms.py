from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import FilledContactForm


class ContactForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        #self.helper.form_action = reverse_lazy('contact')
        #self.helper.form_method = 'POST'
        
        self.helper.form_id = 'contact_form'
        self.helper.attrs  = {
            "hx-post" : reverse_lazy('contact'),
            "hx-target" : '#contact_form',
            "hx-swap" : 'outerHTML'
        }
        self.helper.add_input(Submit('submit', 'Submit'))

    subject = forms.CharField(max_length=32)
    name = forms.CharField(max_length=128)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        print(subject, len(subject))

        if len(subject) <= 3:
            raise forms.ValidationError('Subject to short (should be longer than 3 characters)')

        return subject

    class Meta:
        model = FilledContactForm
        fields = ('name', 'email', 'subject', 'message')


        