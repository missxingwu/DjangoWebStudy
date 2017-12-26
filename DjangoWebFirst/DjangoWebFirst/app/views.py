"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponseRedirect 
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from app import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings

from django.shortcuts import redirect
from django.shortcuts import HttpResponse
import os
import sys
sys.path.append('app/ListTimeToJSon')

import JsonHelp


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })

def adminlogin(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    getss = request.GET
    if request.method == "GET":
       return render(request,
        'adminApp/adminlogin.html')  
    else :
       form = request.POST
       Account = form["Account"]
       PassWord = form["PassWord"]
       # 加密
       pwd = make_password(PassWord)
       # 对比明文和密码是否相同
       ck = check_password("12", pwd)

       # 验证是否存在用户此 Django自带
       user = authenticate(username=Account, password=PassWord)
       Result = False
       if user is not None:
          if user.is_active:
             Result = True
          else:
              Result = False
       else:
          Result = False

       # 返回Json 数据
       name_dict = {'Result': Result, 'Msg': 'I am teaching Django'}
       return JsonResponse(name_dict)
       # 重定向
       #return HttpResponseRedirect('/')
def UpgradeBrowser(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'adminApp/UpgradeBrowser.html')


def fontawesome(request):
    """图标管理"""
    return render(request, 'font-awesome.html')



def upload_file(request):
    returnVal = ""
    Result = False
    Msg = ""
    username = request.POST.get('username')
    try:
         fafafa = request.FILES.get('HeadImgFile')   
         fileName = datetime.now().strftime('%Y%m%d%H%M%S') + JsonHelp.RandomPass().default(6)
         fileName = fileName + "." + fafafa.name.split(".")[1]         
         img_path = os.path.join("static","adminApp","pic",fileName)
         with open(img_path,'wb') as f:
             for item in fafafa.chunks():
               f.write(item)
         Result = True
         returnVal = "/medias/" + fileName
    
    except Exception as err:
           Msg = err.args

    name_dict = {'Result': Result, 'Msg': Msg,'ReturnVal':returnVal}
    return JsonResponse(name_dict)


    