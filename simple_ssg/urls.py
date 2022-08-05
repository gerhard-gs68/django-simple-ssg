from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('download/<str:d_file>/', views.logged_in_download, name='download'),
    path('files/<str:cmd>/<int:file_id>', views.files, name='files')
]
