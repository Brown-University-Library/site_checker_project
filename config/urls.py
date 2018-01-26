# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from site_checker_app import views


admin.autodiscover()


urlpatterns = [

    url( r'^admin/', admin.site.urls ),  # eg host/project_x/admin/

    url( r'^info/$', views.info, name='info_url' ),

    url( r'^status/$', views.show_status, name='show_status_url' ),

    url( r'^$', RedirectView.as_view(pattern_name='info_url') ),

    ]
