from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('thanks_for_sending_message', views.thanks_for_sending_message, name='thanks_for_sending_message'),
    path('download/<str:d_file>/', views.logged_in_download, name='download'),
    path('files/', views.files, name='files'),
    path('add_file/', views.add_file, name='add_file'),
    path('upload_documents/', views.upload_documents, name='upload_documents'),
]
#path('thanks_for_sending_message/', views.)
    
