from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include(('main.urls', 'main'), namespace='main')),
  

]


if settings.DEBUG or not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'HTML2PDF Administrator@Pius_Lucky'
admin.site.site_title = 'HTML2PDF Administrator@Pius_Lucky'
