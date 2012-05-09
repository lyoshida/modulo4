from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    
    
    url(r'catalogar',catalogar, name='catalogar'),
    url(r'editar/(\d+)', editar, name='editar'), 
    url(r'^$', busca, name='busca'),
)
