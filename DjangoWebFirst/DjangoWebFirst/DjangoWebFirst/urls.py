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
import app.user_list

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
    url(r'^admin/user', app.adminviews.user, name='user'), 
    url(r'^admin/add_role$',app.role_list.add_role, name='add_role'),
    url(r'^admin/list_role$', app.role_list.role_list, name='list_role'),
    url(r'^admin/del_role/(\d+)', app.role_list.del_role, name='del_role'),
    url(r'^admin/perm_role/(\d+)', app.role_list.perm_role, name='perm_role'),

    
    url(r'^admin/list_user$',app.user_list.list, name='list_user'),
    url(r'^admin/add_user$', app.user_list.edit, name='add_user'),
    url(r'^admin/del_user/(\d+)', app.user_list.del_user, name='del_user'),
    url(r'^admin/perm_user/(\d+)', app.user_list.role, name='perm_user'),
    url(r'^admin/permroledata$', app.user_list.rolepost, name='permroledata'),

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
