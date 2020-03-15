from django.urls import path, re_path, include
from main.views import (
home,
postUrlForm,
finalLogic
)
urlpatterns = [
		# path(r'', landing, name="landing"),
		path(r'', home, name="landing"),
		path('post/urlform/', postUrlForm, name ='url_form_submit'),
		path(r'page/<int:id>.pdf/', finalLogic, name="pdf")
		]

