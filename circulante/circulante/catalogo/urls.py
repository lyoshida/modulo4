from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    
    url(r'busca', busca, name='busca'),
    url(r'catalogar',catalogar, name='catalogar'),
    url(r'editar/(\d+)', editar, name='editar'), 
)
