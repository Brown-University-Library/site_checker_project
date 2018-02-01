# -*- coding: utf-8 -*-

from django.contrib import admin
from site_checker_app.models import CheckSite


class CheckSiteAdmin( admin.ModelAdmin ):
    save_on_top = True
    list_display = [ 'name', 'partial_url', 'partial_text', 'recent_checked_time', 'recent_checked_result', 'next_check_time' ]
    ordering = [ 'name' ]
    search_fields = [ 'name', 'url', 'email_addresses' ]
    readonly_fields = (
        'calculated_seconds',
        'recent_checked_time',
        'recent_checked_result',
        'previous_checked_result',
        'pre_previous_checked_result',
        'next_check_time',
        )
    fieldsets = (
        ('editable', {
            'classes': ('wide',),
            'fields': (
                'name',
                'url',
                'text_expected',
                'check_frequency_number',
                'check_frequency_unit',
                'email_addresses',
                'email_message',
            )
        }),
        ('not-editable', {
            'classes': ('wide',),
            'fields': (
                'calculated_seconds',
                'recent_checked_time',
                'next_check_time',
                'recent_checked_result',
                'previous_checked_result',
                'pre_previous_checked_result',
            ),
        }),
    )

    def partial_url(self, obj):
        """ Specifies appearance of url in list_display. """
        p_url = ''
        if len(obj.url) <= 50:
            p_url = obj.url
        else:
            p_url = '%s...' % obj.url[0:47]
        return p_url
    partial_url.short_description = 'url'

    def partial_text(self, obj):
        """ Specifies appearance of text_expected in list_display. """
        expected = ''
        if len(obj.text_expected) <= 50:
            expected = obj.text_expected
        else:
            expected = '%s...' % obj.text_expected[0:47]
        return expected
    partial_text.short_description = 'text_expected'

    ## end class CheckSiteAdmin()


admin.site.register( CheckSite, CheckSiteAdmin )
