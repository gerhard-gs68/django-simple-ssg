from django.contrib import admin
from .models import FilledContactForm, Files

# Register your models here.
admin.site.register(FilledContactForm)
admin.site.register(Files)