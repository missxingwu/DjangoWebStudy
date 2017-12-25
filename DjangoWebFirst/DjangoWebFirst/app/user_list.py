from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponseRedirect 
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password #加密解密
from django.core import serializers
from app import models
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #分页
import json
from django.forms.models import model_to_dict  # 模型转为字典
import time
from django.db.models  import  Q 
import sys
sys.path.append('app/ListTimeToJSon')

import JsonHelp

from django.db import transaction #事务
def lists(request):
    fullname = request.GET.get('FullName')    
    sex = request.GET.get('Sex')  
    columns = models.Sys_User.objects.all() #models.Sys_Role.objects.filter(IsDeleted=False)
    if fullname != None and fullname != "": 
      columns = models.Sys_User.objects.filter(IsDeleted=False).filter(Q(Account__contains=fullname) | Q(FullName__contains=fullname) | Q(Email__contains=fullname) | Q(Phone__contains=fullname))
    if sex != None and sex != "":
        columns = columns.filter(Sex=sex)
    
    if sex != None or sex != "":
        # lanmbda 表达式过滤数据
        cos = list(tuple(filter(lambda x: x.Sex == bool(sex),columns)))
    total = int(request.GET.get('PageSize')) # 每页最多显示数据量
    if total <= 0:
        total = 2

    totalCount = len(columns)                # 总数据量
    totalPage = int(totalCount / total)      # 总页数
    if totalCount % total > 0:
        totalPage+=1
    
    
    paginator = Paginator(columns, total)

    page = request.GET.get('PageIndex')
   
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)

    result_list = []
    for row in customer.object_list:
        rowJson = model_to_dict(row)
        #rowJsonData = json.dumps(rowJson, cls =
        #JsonHelp.DateEncoder,ensure_ascii=False) 测试序列化
        result_list.append(rowJson)
    
  
    name_dict = {"rows": result_list, "total": total,"totalCount":totalCount,"totalPage":totalPage}
    return JsonResponse(name_dict)

def edit(request):
    """用户新增和修改"""
    #assert isinstance(request, HttpRequest)
    use2r = request.session.get(settings.ADMIN_SESSION,default=None)
    if use2r is None:
        return HttpResponseRedirect('/adminlogin')
    keyId = 0
    try:
         keyId = int(request.GET.get('KeyId'))
    except Exception as err:
          keyId = 0    
          
    if request.method == "GET":
       try:
            roleModel = models.Sys_User.objects.get(KeyId=keyId)
       except Exception as err:
           roleModel = None       
       if keyId > 0 and roleModel != None:
           return render(request,
                 'adminApp/user_add.html',{
                     'Model':roleModel,
                     'title':'修改'})
       else:
           return render(request,'adminApp/user_add.html',{'Model':models.Sys_User(KeyId=0),'title':'新增'})  
    else :
       form = request.POST
       keyId = int(form["KeyId"])
       Result = False    
       Msg = ""
       try:
          if keyId > 0:
              userBykeyId = models.Sys_User.objects.filter(KeyId=keyId).first()
              sys_user_form = models.Sys_User_Form(request.POST,instance=userBykeyId)
              if sys_user_form.is_valid():
                  sys_user_form.save()
                  Result = True  
             
          else:
              pwd = form["PassWord"]
              sys_user_form = models.Sys_User_Form(request.POST)
              if sys_user_form.is_valid():
                  userPost = sys_user_form.save(commit=False) #在sys_user_form.save(commit=False时，添加一些表单中未有的数据)
                  userPost.PassWord = make_password(pwd)  
                  userPost.Job = "手动测试数据"
                  userPost.save()
                  Result = True  
                 
       except Exception as err:
           Result = False 
           Msg = err.args
     
       # 返回Json 数据
       name_dict = {'Result': Result, 'Msg': Msg}
       return JsonResponse(name_dict)

def del_user(request,keyId):
     """删除用户"""
     use2r = request.session.get(settings.ADMIN_SESSION,default=None)
     if use2r is None:
        return HttpResponseRedirect('/adminlogin')
     Result = False    
     Msg = ""
     try:
            roleModel = models.Sys_User.objects.filter(KeyId=keyId).delete()
            Result = True
     except Exception as err:
           Msg = err.args     

     name_dict = {'Result': Result, 'Msg': Msg}
     return JsonResponse(name_dict)

def role(request,keyId):
    """分配角色 """
    if request.method == "GET":
        roleModel = models.Sys_Role.objects.filter(IsDeleted=False)
        return render(request,'adminApp/user_role.html',{
                         'model':roleModel,
                         'title':'分配角色',
                         'userId':keyId})

#@transaction.atomic
def rolepost(request):
    """分配角色 """
    if request.method == "POST":
        form = request.POST
        keyId = form["UserId"]
        RoleIds = form["RoleIds"]
        #RoleIds = RoleIds.rstrip().replace()
        listRoleId = RoleIds.split(",")
        Result = False
        Msg = ""
       

        count = 0
        try:
            with transaction.atomic():
              userrole_list_to_insert = []
              while count < (len(listRoleId) - 1):                     
                       userrole = models.Sys_UserRole(UserId=keyId,RoleId=listRoleId[count],DateTime=datetime.now())
                       userrole_list_to_insert.append(userrole)
                       count = count + 1
              
              models.Sys_UserRole.objects.filter(UserId =keyId).delete()
              models.Sys_UserRole.objects.bulk_create(userrole_list_to_insert)
              Result = True    
        except Exception as err:
            Result = False
            Msg = err.args

        name_dict = {'Result': Result, 'Msg': Msg}
        return JsonResponse(name_dict)
    elif request.method == "GET":
        keyId = request.GET.get('UserId')
        userrolelist = models.Sys_UserRole.objects.filter(UserId =keyId)    
        if len(userrolelist) < 1:
             return JsonResponse("",safe=False)
        jsondata = serializers.serialize("json",userrolelist,ensure_ascii = False)
        return JsonResponse(jsondata,safe=False)


def password(request):
    """用户密码修改"""
    #assert isinstance(request, HttpRequest)
    use2r = request.session.get(settings.ADMIN_SESSION,default=None)
    if use2r is None:
        return HttpResponseRedirect('/adminlogin')
    """  字典转模型  
       useceshi = request.session.get("ceshisession",default=None)
       back = json.loads(useceshi)
       back2 = models.Sys_User(**back)
    """

    if request.method == "GET":
       try:
            roleModel = models.Sys_User.objects.get(KeyId=keyId)
       except Exception as err:
           roleModel = None       
       return render(request,'adminApp/user_pwd.html',{'Model':models.Sys_User(KeyId=0),'title':'新增'})  
    else :
       form = request.POST
       oldPwd = form["OldPwd"]
       newPwd = form["NewPwd"]
       Result = False    
       Msg = ""

       for obj in serializers.deserialize("json", use2r):
          
          try:
             if obj.object.KeyId > 0:
                 userBykeyId = models.Sys_User.objects.get(KeyId=obj.object.KeyId)
                 if check_password(oldPwd, userBykeyId.PassWord):
                     userBykeyId.PassWord = make_password(newPwd)
                     userBykeyId.save()
                     """更新Session"""
                     user = serializers.serialize("json", models.Sys_User.objects.filter(Account=userBykeyId.Account))                    
                     request.session[settings.ADMIN_SESSION] = user
                     Result = True                  
                    
          except Exception as err:
                 Result = False 
                 Msg = err.args

       
       
     
       # 返回Json 数据
       name_dict = {'Result': Result, 'Msg': Msg}
       return JsonResponse(name_dict)