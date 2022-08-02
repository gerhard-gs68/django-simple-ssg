from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('download/<str:d_file>/', views.download, name='download'),
    path('download/', views.download, name='download'),
]
