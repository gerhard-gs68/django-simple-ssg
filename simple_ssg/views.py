from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth.decorators import login_required, user_passes_test  
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse_lazy
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form

from .models import FilledContactForm, Files
from .forms import ContactForm

from pathlib import Path

# Create your views here.
def contact(request):
    
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            send_mail(
                form.cleaned_data['subject'],
                f"from {form.cleaned_data['name']}, ({form.cleaned_data['email']})\n\n{form.cleaned_data['message']}",
                 'supidupihall@blueberrye.io',
                ['gerhard.spitzlsperger@lfoundry.com'],
                 fail_silently=False,
            )

            template = render(request, 'thanks_for_sending_message.html')
            template['Hx-Push'] = '/thanks_for_sending_message/'
            return template

        # this is only executed if form is not valid
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)

    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'cform' : form}) 




def thanks_for_sending_message(request):
    return render(request, 'thanks_for_sending_message.html')  
        

@login_required
def files(request):
    all_files  = Files.objects.all().filter(user__username=request.user.username)


    return render(request, 'files.html', {'files' : all_files}) 

@login_required
def add_file(request):
    if request.method == 'POST':
        my_file = request.FILES.get('the_file')
        
        # add film
        the_file = Files.objects.create(user=request.user, 
                                        the_file=my_file,
                                        file_name=my_file.name)
                              
        the_file.save()
        
        # add the film to the user's list
        #request.user.files.add(the_file)

        files = Files.objects.all().filter(user__username=request.user.username)

        # return template fragment with all the user's films
        
        return render(request, 'file_list.html', {'files': files})


# @login_required
# def files(request, cmd, file_id):
#     print(settings.USER_DIR_BASE)
#     base_user_dir = Path(settings.USER_DIR_BASE) / str(request.user.username)
     
#     the_files = [{
#                 'name' : 'Home',
#                 'rel_path' : '.',
#                 'suffix' : '',
#                 'is_dir' : True,
#                 'is_file' : False,
#                 'file_id' : 0,
#                 'owner' : 0,
#                 'level' : 0,
#                 'ident_str' : ''
#             }]

#     if request.user.is_staff:
#         base_user_dir = base_user_dir.parent

    

   
#     def traverse_files(the_dir, the_files, count, owner, level):

#         for child in the_dir.iterdir():
#             if child.name == '.DS_Store':
#                 continue

#             rel_path = child.relative_to(base_user_dir)
#             print("RELPATH", rel_path.parent)

#             count += 1
            
#             the_files.append({
#                 'name' : child.name,
#                 'rel_path' : str(rel_path.parent),
#                 'suffix' : child.suffix,
#                 'is_dir' : child.is_dir(),
#                 'is_file' : child.is_file(),
#                 'file_id' : count,
#                 'owner' : owner,
#                 'ident_str' : level * '&nbsp;'
#             })
#             #print(the_files[-1])

#             if child.is_dir():
#                 new_level = level+1
#                 the_files = traverse_files(child, the_files, count, count, new_level)

#         return the_files

#     the_files = traverse_files(the_dir=base_user_dir, the_files=the_files, count=0, owner=0, level=0)
#     print(the_files)

#     return render(request, 'files.html', {'files' : the_files}) 

