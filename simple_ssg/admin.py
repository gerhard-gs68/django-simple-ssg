from django.contrib import admin
from .models import FilledContactForm, Documents, Files

# Register your models here.
admin.site.register(FilledContactForm)
admin.site.register(Documents)
admin.site.register(Files)