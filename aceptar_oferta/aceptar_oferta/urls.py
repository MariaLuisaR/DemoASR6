from django.urls import path
from . import views
urlpatterns = [
    path('', views.upload_file, name='upload_file'),  
    path('aceptar_oferta/<int:pk>/', views.aceptar_oferta, name='aceptar_oferta'),  
    path('enviar_email/', views.enviar_email, name='enviar_email'), 
    path('correo_enviado/', views.correo_enviado, name='correo_enviado'),

]
