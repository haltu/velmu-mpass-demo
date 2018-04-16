
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


class AdminSite(admin.AdminSite):
  def has_permission(self, request):
    return request.user.is_active and request.user.is_staff and request.user.is_superuser

admin.site = AdminSite()
admin.autodiscover()


admin_urls = [
  url(r'^sysadmin/', include(admin.site.urls)),
]

app_urls = [
  url(r'^', include('dreamcards.urls.desktop')),
  url(r'^uiapi/1/', include('dreamcards.urls.uiapi')),
]

auth_urls = [
  url(r'login/mpass/', include('mpass.urls.login')),
  url(r'^', include('django.contrib.auth.urls')),
  url(r'', include('dreamsso.urls')),
]

monitor_urls = [
  url(r'^monitor/', include('health_check.urls')),
]

static_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_urls += staticfiles_urlpatterns()

urlpatterns = admin_urls + app_urls + static_urls + auth_urls + monitor_urls

if settings.DEBUG:
  from django.views.generic import TemplateView
  urlpatterns += [
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    url(r'^503/$', TemplateView.as_view(template_name='503.html')),
  ]

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

