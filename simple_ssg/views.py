from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import FilledContactForm
from .forms import ContactForm

from pathlib import Path

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

            send_mail(
                form.cleaned_data['subject'],
                f"from {form.cleaned_data['name']}, ({form.cleaned_data['sender']})\n\n{form.cleaned_data['message']}",
                 'supidupihall@blueberrye.io',
                ['gerhard.spitzlsperger@lfoundry.com'],
                 fail_silently=False,
            )

            return HttpResponseRedirect('/thanks/')

    else:
        form = ContactForm()
        
      

    return render(request, 'contact.html', {'cform' : form}) 




def download(request, d_file= "default_file"):
    print(d_file)
                
    return FileResponse(open("./media/datasheet.PDF", 'rb'), as_attachment=True)


@login_required
def logged_in_download(request, d_file="default_file"):
    return download(request, d_file)

@login_required
def files(request, cmd, file_id):
    print(settings.USER_DIR_BASE)
    base_user_dir = Path(settings.USER_DIR_BASE) / str(request.user.username)
     
    the_files = [{
                'name' : 'Home',
                'rel_path' : '.',
                'suffix' : '',
                'is_dir' : True,
                'is_file' : False,
                'file_id' : 0,
                'owner' : 0,
                'level' : 0,
                'ident_str' : ''
            }]

    if request.user.is_staff:
        base_user_dir = base_user_dir.parent

    

   
    def traverse_files(the_dir, the_files, count, owner, level):

        for child in the_dir.iterdir():
            if child.name == '.DS_Store':
                continue

            rel_path = child.relative_to(base_user_dir)
            print("RELPATH", rel_path.parent)

            count += 1
            
            the_files.append({
                'name' : child.name,
                'rel_path' : str(rel_path.parent),
                'suffix' : child.suffix,
                'is_dir' : child.is_dir(),
                'is_file' : child.is_file(),
                'file_id' : count,
                'owner' : owner,
                'ident_str' : level * '&nbsp;'
            })
            #print(the_files[-1])

            if child.is_dir():
                new_level = level+1
                the_files = traverse_files(child, the_files, count, count, new_level)

        return the_files

    the_files = traverse_files(the_dir=base_user_dir, the_files=the_files, count=0, owner=0, level=0)
    print(the_files)

    return render(request, 'files.html', {'files' : the_files}) 






