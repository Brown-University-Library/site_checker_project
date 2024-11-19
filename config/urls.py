# -*- coding: utf-8 -*-

from django.urls import path, re_path
from django.contrib import admin
from django.views.generic import RedirectView
from site_checker_app import views


admin.autodiscover()


urlpatterns = [

    ## primary app urls
    re_path( r'^admin/', admin.site.urls ),  # eg host/project_x/admin/
    path( 'status/', views.show_status, name='show_status_url' ),
    # url( r'^status_old/$', views.show_status_old, name='show_status_old_url' ),
    path( 'login/', views.login, name='admin_login_url' ),

    ## info urls
    path( 'error_check/', views.error_check, name='error_check_url' ),
    path( 'info/', views.info, name='info_url' ),

    ## support urls
    path( 'bul_search/', views.bul_search, name='bul_search_url' ),

    path( '', RedirectView.as_view(pattern_name='show_status_url') ),

    ]
