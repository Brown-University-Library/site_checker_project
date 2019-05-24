# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from site_checker_app import views


admin.autodiscover()


urlpatterns = [

    ## primary app urls
    url( r'^admin/', admin.site.urls ),  # eg host/project_x/admin/
    url( r'^status/$', views.show_status, name='show_status_url' ),
    # url( r'^status_old/$', views.show_status_old, name='show_status_old_url' ),
    url( r'^login/$', views.login, name='admin_login_url' ),

    ## info urls
    url( r'^error_check/$', views.info, name='error_check_url' ),
    url( r'^info/$', views.info, name='info_url' ),

    ## support urls
    url( r'^bul_search/$', views.bul_search, name='bul_search_url' ),

    url( r'^$', RedirectView.as_view(pattern_name='show_status_url') ),

    ]
