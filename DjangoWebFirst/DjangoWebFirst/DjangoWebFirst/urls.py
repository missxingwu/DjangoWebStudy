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
import app.button_list
import app.views_menu
from django.views.static import serve

from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()


urlpatterns = [# Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^admin/upload$', app.views.upload_file, name='upload'), 
    #url(r'^medias/(?P<path>.*)$', serve, {'document_root': "D:\\save\\Pythons\\DjangoWebStudy\\DjangoWebFirst\\DjangoWebFirst\\static\\adminApp\\pic"}), 
    #url(r'^adminlogin', app.views.adminlogin, name='adminlogin'),
    #url(r'^UpgradeBrowser', app.views.UpgradeBrowser,
    #name='UpgradeBrowser'),upload
    url(r'^admin/index', app.adminviews.home, name='index'),
    url(r'^admin/main', app.adminviews.main, name='main'),
    url(r'^admin/role', app.adminviews.role, name='role'),  
    url(r'^admin/user', app.adminviews.user, name='user'), 
  

    # 角色管理
    url(r'^admin/perm/permissions$',app.role_list.permissions,name='permissions'),

    url(r'^admin/add_role$',app.role_list.add_role, name='add_role'),
    url(r'^admin/list_role$', app.role_list.role_list, name='list_role'),
    url(r'^admin/del_role/(\d+)', app.role_list.del_role, name='del_role'),
    url(r'^admin/perm_role/(\d+)', app.role_list.perm_role, name='perm_role'),
   

     # 用户管理
    url(r'^admin/list_user$',app.user_list.lists, name='list_user'),
    url(r'^admin/add_user$', app.user_list.edit, name='add_user'),
    url(r'^admin/del_user/(\d+)', app.user_list.del_user, name='del_user'),
    url(r'^admin/perm_user/(\d+)', app.user_list.role, name='perm_user'),
    url(r'^admin/permroledata$', app.user_list.rolepost, name='permroledata'),
    url(r'^admin/pwd/password$',app.user_list.password,name='pwd_user'),

   

    # 按钮管理
    url(r'^admin/button/index',app.button_list.index, name='button'),
    url(r'^admin/button/listdata$', app.button_list.listdata, name='list_button'),
    url(r'^admin/button/edit$', app.button_list.edit, name='edit_button'),
    url(r'^admin/button/delete/(\d+)', app.button_list.delete, name='delete_button'),
    url(r'^admin/button',app.button_list.index, name='button'),

     # 菜单管理
    url(r'^admin/menu/index',app.views_menu.index, name='menu'),
    url(r'^admin/menu/listdata$', app.views_menu.listdata, name='list_menu'),
    url(r'^admin/menu/edit$', app.views_menu.edit, name='edit_menu'),
    url(r'^admin/menu/delete/(\d+)', app.views_menu.delete, name='delete_menu'),
    url(r'^admin/menu/button/(\d+)', app.views_menu.button, name='menubutton'),
    url(r'^admin/menu/savebutton', app.views_menu.savebutton, name='buttonlist'),
    url(r'^admin/menu',app.views_menu.index, name='menu'),

   

    url(r'^adminlogin', app.adminviews.adminlogin, name='adminlogin'),
    url(r'^UpgradeBrowser', app.adminviews.UpgradeBrowser, name='UpgradeBrowser'),
    url(r'^font-awesome', app.views.fontawesome, name='font-awesome'),
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
    url(r'^admin/', include(admin.site.urls)),]

# 图片显示路径
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  
