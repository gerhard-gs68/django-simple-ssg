from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('thanks_for_sending_message', views.thanks_for_sending_message, name='thanks_for_sending_message'),
    path('files/', views.files, name='files'),
    path('add_file/', views.add_file, name='add_file'),
]
#path('thanks_for_sending_message/', views.)
    
