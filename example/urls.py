from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
from django.views.generic.base import TemplateView
from example_app import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^registrations/(?P<username>\w+)', views.RegistrationView.as_view(), name='registration'),
    url(r'^registration_thanks', TemplateView.as_view(template_name='example_app/registration_thanks.html'),name='registration_thanks'),
    url(r'^mvtester/', include('mvtester.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register$', views.RegisterView.as_view(),name='register'),
    url(r'^$', TemplateView.as_view(template_name='index.html'),name='home')
)

urlpatterns = urlpatterns + patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    ) if settings.DEBUG else urlpatterson

