from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = "index"),
    path('save_conversation/', views.save_conversation, name='save_conversation'),
    path('generate_soap/', views.generate_soap, name='generate_soap'),
    path('save_soap/', views.save_soap, name='save_soap'),
    
]
