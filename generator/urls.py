from django.urls import path
from . import views


urlpatterns = [

    # Root → Direct Mural AI
    path('', views.home, name='home'),

    # AI Generators
    path('mural/', views.mural, name='mural'),
    path('painting/', views.painting, name='painting'),
    path('general/', views.general, name='general'),


]