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
from django.core import serializers
from app import models
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 登录页面
def adminlogin(request):
    """Renders the adminlogin page."""
    #assert isinstance(request, HttpRequest)
    use2r = request.session.get(settings.ADMIN_SESSION,default=None)
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
       userModel = models.Sys_User.objects.get(Account=Account,IsDeleted=False)
       Result = False
       if userModel is not None:
          if check_password(PassWord, userModel.PassWord):
             user = serializers.serialize("json", models.Sys_User.objects.filter(Account=Account))
             user2 = userModel.toJSONDateTime()
             request.session[settings.ADMIN_SESSION] = user
             Result = True
          else:
              Result = False
       else:
          Result = False

       # 返回Json 数据
       name_dict = {'Result': Result, 'Msg': 'I am teaching Django'}
       return JsonResponse(name_dict)

def UpgradeBrowser(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'adminApp/UpgradeBrowser.html')

# 首页
def home(request):
    #assert isinstance(request, HttpRequest)
    user = request.session.get(settings.ADMIN_SESSION,default=None)
    if user is None:
        return HttpResponseRedirect('/adminlogin')

    account = ""
    for obj in serializers.deserialize("json", user):
        if obj.object.KeyId == 1:
            account = obj.object.Account
        

    sysUser = models.Sys_User.objects.get(Account=account,IsDeleted=False)
    if sysUser is None:
        return HttpResponseRedirect('/adminlogin')
    
    allMenus = models.Sys_Menu.objects.with_counts()
    topMenus = list(filter(lambda x: x.AccountId == sysUser.KeyId and x.IsDeleted == False and x.IsRoot == True,allMenus))
    leftMenus = list(filter(lambda x: x.AccountId == sysUser.KeyId and x.IsDeleted == False and x.IsRoot == False,allMenus))
    if sysUser.HeadImg is None or sysUser.HeadImg == "":
        sysUser.HeadImg = "/Content/jeui/images/photo2.jpg"
    
    #menus = filter(lambda x: x.AccountId==sysUser.KeyId,
    #models.Sys_Menu.objects.with_counts())
    return render(request,
        'adminApp/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'topMenus':topMenus,
            'leftMenus':leftMenus,
            'LoginName':sysUser.FullName,
            'LoginImg':sysUser.HeadImg,
        })

def main(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'adminApp/main.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })


def role(request):
    """角色页面"""
    assert isinstance(request, HttpRequest)
    return render(request,
        'adminApp/Role.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

def  user(request):
    """用户页面"""
    assert isinstance(request, HttpRequest)
    return render(request,
        'adminApp/user.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

