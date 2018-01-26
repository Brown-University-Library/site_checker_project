# -*- coding: utf-8 -*-

from django.contrib import admin
from site_checker_app.models import CheckSite


class CheckSiteAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [ 'name', 'url', 'text_expected', 'recent_checked_time', 'recent_checked_result', 'next_check_time' ]
    ordering = [ 'name' ]


admin.site.register( CheckSite, CheckSiteAdmin )
