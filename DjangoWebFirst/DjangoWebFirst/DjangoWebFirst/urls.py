"""
Definition of urls for DjangoWebFirst.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
import app.adminviews
import app.role_list

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    #url(r'^adminlogin', app.views.adminlogin, name='adminlogin'),
    #url(r'^UpgradeBrowser', app.views.UpgradeBrowser, name='UpgradeBrowser'),
    url(r'^admin/index', app.adminviews.home, name='index'),
    url(r'^admin/main', app.adminviews.main, name='main'),
    url(r'^admin/role', app.adminviews.role, name='role'),
    url(r'^admin/list_role$', app.role_list.role_list, name='list_role'),
    url(r'^adminlogin', app.adminviews.adminlogin, name='adminlogin'),
    url(r'^UpgradeBrowser', app.adminviews.UpgradeBrowser, name='UpgradeBrowser'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
