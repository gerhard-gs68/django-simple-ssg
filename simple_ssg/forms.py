from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=32)
    name = forms.CharField(max_length=128)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
   
