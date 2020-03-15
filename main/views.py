from __future__ import absolute_import
import os
import requests
import convertapi
import tempfile
from django.urls import reverse
from django.shortcuts import render
from main.forms import URLForm
from main.models import URL
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from main.models import Footer



def home(request):
	template = "index.html"
	c_obj = Footer.objects.all()
	for only_item in c_obj:
		start_year = only_item.start_year
		current_year = only_item.current_year
	# I already printed the form and used all of its 
	# attributes in a form in index.html, there is no point
	# passing it into our context variable
	form = URLForm()
	try:
		return render(request, template, {"start_year":start_year, "current_year":current_year})
	except UnboundLocalError:
		return render(request, template, {})

def postUrlForm(request):
	if request.method == "POST" and request.is_ajax():
		form = URLForm(request.POST or None, request.FILES or None)
		if form.is_valid(): 
			instance = form.save(commit=False)
			instance.save()
			d_link = u'{0}/page/{1}.pdf/'.format(settings.DOMAIN_NAME, instance.id)
			success_msg = "Status: Processing..." 
			return JsonResponse({"success":True, "download_link":d_link, "success_msg":success_msg}, status=200)           
		else:
			msg = "Invalid link, use link like https://google.com"
			form = URLForm()
			return JsonResponse({"success":False, "msg":msg}, status=400) 
	return JsonResponse({"success":False}, status=400)
   

def finalLogic(request, id):
	convertapi.api_secret = settings.CONVERT_API_SECRET
	url_object = get_object_or_404(URL, id=id)
	try:
		r = requests.get(url_object)
		status = r.status_code
		url_str = str(url_object)
		if status == 200 and "http" or "https" in url_str:
			link_name = str(url_object).split("://")[1].split("/")[0]
			filename = '{0}_{1}'.format(link_name, id)
			# now let's use the convertAPI
			output_format = "pdf"
			input_format = "web"
			try:
				result = convertapi.convert(
				    output_format,
				    {
				        'Url': url_str,
				        'FileName': filename,
				    },
				    from_format = input_format,
				    timeout = 180,
				)
				full_path = str(settings.MEDIA_ROOT)
				# save to file
				result.file.save(full_path)
				# clean existing records in the media directory
				for each_file in os.listdir(full_path):
					if not filename in each_file:
						full_path_remove =  os.path.join(settings.MEDIA_ROOT, str(each_file))
						os.remove(full_path_remove)
				# cleaning existing records in our database
				other_objects = URL.objects.exclude(id=id)
				for all_others in other_objects:
					all_others.delete()
					# clean existing records in the media directory
					for each_file in os.listdir(full_path):
						if not filename in each_file:
							full_path_remove =  os.path.join(settings.MEDIA_ROOT, str(each_file))
							os.remove(full_path_remove)
				media_url = settings.MEDIA_URL
				domain_name = settings.DOMAIN_NAME
				pdf_full_name = u"{0}.pdf".format(filename)
				full_pdf_link = "{0}{1}{2}".format(domain_name, media_url, pdf_full_name)
				success_msg = "<html>Status: <span style='color:green;'>Done!</span></html>"
				return JsonResponse({"success":True, "pdf_link":full_pdf_link, "msg":success_msg}, status=200)
			except ConnectionError:
				status ="<html>Status: <em><span style='color:red;'>Failed!</span></em></html>"
				con_err_msg = "Link could not be accessed, check internet connection!"
				return JsonResponse({"success":False, "msg":con_err_msg, "status":status}, status=400)

		elif status == 400 and "http" or "https" in url_str:
			status ="<html>Status: <em><span style='color:red;'>Failed!</span></em></html>"
			con_err_msg = "Link must have been broken somehow :), Try with a valid link"
			return JsonResponse({"success":False, "msg":con_err_msg, "status":status}, status=400) 
		elif status == 404 and "http" or "https" in url_str:
			status ="<html>Status: <em><span style='color:red;'>Failed!</span></em></html>"
			con_err_msg = "Link is no longer available :), It must have been moved/deleted!"
			return JsonResponse({"success":False, "msg":con_err_msg, "status":status}, status=400) 
		else:
			# clean existing records in database when errors occur
			other_objects = URL.objects.exclude(id=id)
			for all_others in other_objects:
				all_others.delete()
			status ="<html>Status: <em><span style='color:red;'>Failed!</span></em></html>"
			con_err_msg = "Link could not be accessed, check internet connection!"
			return JsonResponse({"success":False, "msg":con_err_msg, "status":status}, status=400)
	except ConnectionError:
		status ="<html>Status: <em><span style='color:red;'>Failed!</span></em></html>"
		con_err_msg = "Link could not be accessed, check internet connection!"
		return JsonResponse({"success":False, "msg":con_err_msg, "status":status}, status=400)

