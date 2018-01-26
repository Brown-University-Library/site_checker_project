# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect

log = logging.getLogger(__name__)


class CheckSite(models.Model):

    FREQUENCY_UNIT_CHOICES = (
        ('minute', 'Minute'),
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('month', 'Month'),
        )
    name = models.CharField( max_length=50, help_text='''(i.e. 'Josiah home-page' or 'patron_api')''' )
    url = models.URLField( max_length=200 )
    response_expected = models.PositiveIntegerField( editable=False, null=True, blank=True, help_text='''for if you want to test the response code, like '200' ('OK')''' )  # for if you want to test the response code, like '200' ('OK')
    text_expected = models.TextField()
    check_frequency_number = models.PositiveIntegerField( help_text='(More-frequent checks increase server load)' )
    check_frequency_unit = models.CharField( max_length=10, choices=FREQUENCY_UNIT_CHOICES, default='hour' )
    calculated_seconds = models.PositiveIntegerField( editable=False )  # stores calculated frequence in seconds
    email_addresses = models.TextField( help_text='(Separate multiple email-addresses with a comma, like aaa@example.com, bbb@example.com)' )
    email_message = models.TextField( help_text='(Will be included in body of email)' )
    recent_checked_time = models.DateTimeField( null=True, blank=True, help_text='''(Set automatically)''' )
    recent_checked_result = models.CharField( max_length=50, blank=True, help_text='''(Set automatically)''' )
    previous_checked_result = models.CharField( max_length=50, editable=False )
    pre_previous_checked_result = models.CharField( max_length=50, editable=False )
    next_check_time = models.DateTimeField( null=True, blank=True, help_text='''(Set automatically)''' )  # stores calculated recent_checked_time + calculated_seconds

    def __unicode__(self):
        return self.name

    def save(self):
        # fill in recent_checked_time with current date if necessary
        if ( self.recent_checked_time == None ):
            import datetime
            self.recent_checked_time = datetime.datetime( 2000, 01, 15 )
        # update calculated_seconds
        self.calculated_seconds = self.createDeltaSeconds( self.check_frequency_number, self.check_frequency_unit )
        # update next_check_time
        self.next_check_time = self.createDeltaTime( self.recent_checked_time, self.calculated_seconds )
        # call the real save method
        super(CheckSite, self).save()

    def createDeltaSeconds( self, frequency_integer, unit_string ):
        minute_value = 60
        hour_value = minute_value * 60
        day_value = hour_value * 24
        month_value = 365 / 12
        unit_dict = {'minute': minute_value, 'hour': hour_value, 'day': day_value, 'month': month_value}
        return unit_dict[unit_string] * frequency_integer

    def createDeltaTime( self, start_time, delta_seconds ):
        import datetime
        normal_time_delta = datetime.timedelta(seconds=delta_seconds)
        if ( self.recent_checked_result == 'passed' ):
            time_delta = normal_time_delta
        else: # on failure check at least every five minutes
            default_error_recheck_delta = datetime.timedelta( minutes = 2 )
            if ( normal_time_delta < default_error_recheck_delta ):
                time_delta = normal_time_delta
            else:
                time_delta = default_error_recheck_delta
        return start_time + time_delta

    class Meta:
        ordering = ['name']
        verbose_name_plural = "CheckSite Entries"

    ## end class CheckSite()
