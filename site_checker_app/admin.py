# -*- coding: utf-8 -*-

from django.contrib import admin
from site_checker_app.models import CheckSite


class CheckSiteAdmin( admin.ModelAdmin ):
    save_on_top = True
    list_display = [ 'name', 'partial_url', 'text_expected', 'recent_checked_time', 'recent_checked_result', 'next_check_time' ]
    ordering = [ 'name' ]

    def partial_url(self, obj):
        """ Specifies appearance of url in list_display. """
        p_url = ''
        if len(obj.url) <= 50:
            p_url = obj.url
        else:
            p_url = '%s...' % obj.url[0:47]
        return p_url
    partial_url.short_description = 'url'


admin.site.register( CheckSite, CheckSiteAdmin )
