from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('lists.views',
     url(r'^new$', 'new_list', name='new_list'),
     url(r'^(\d+)/$', 'view_list', name='view_list'),
     url(r'^(\d+)/add-item$', 'add_item', name='add_item'),
)
