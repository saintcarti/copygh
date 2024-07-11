from django.urls import path
from .views import vistaIndex,vistaNosotros

urlpatterns=[
    path('',vistaIndex,name="Inicio"),
    path('nosotros/',vistaNosotros,name="Nosotros"),
    
]