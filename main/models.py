import os
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from main.logic import current_year


class URL(models.Model):
	url = models.URLField(blank=False, null=False, max_length=5000 )
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	def __str__(self):
	    return str(self.url)
	class Meta:
		ordering = ["-timestamp"]



class Footer(models.Model):
	current_year = models.CharField(
	verbose_name=_('current_year'), max_length=4,
	default = current_year
	)
	start_year = models.CharField(
	verbose_name=_('start_year'), max_length=4,
	default = 2020)

	def __str__(self):
	    return u'start year: {0}, current: {1}'.format(self.start_year, self.current_year)