from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import FilledContactForm
from .forms import ContactForm


# Create your views here.
def contact(request):
    
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = FilledContactForm()
            
            contact.subject = form.cleaned_data['subject']
            contact.name = form.cleaned_data['name']
            contact.email = form.cleaned_data['sender']
            contact.message = form.cleaned_data['message']
            contact.save()


            return HttpResponseRedirect('/thanks/')

    else:
        form = ContactForm()
        
      

    return render(request, 'contact.html', {'cform' : form}) 
