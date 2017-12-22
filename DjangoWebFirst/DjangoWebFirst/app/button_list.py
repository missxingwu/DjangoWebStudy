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
def index(request):
    """按钮管理"""
    return render(request, 'adminApp/button/index.html',{'title':'按钮管理'}) 

def listdata(request):
    """按钮列表"""
    fullname = request.GET.get('FullName')    
  
    columns = models.Sys_Button.objects.filter(IsDeleted=False) #models.Sys_Role.objects.filter(IsDeleted=False)
    if fullname != None and fullname != "": 
      columns = columns.filter(Q(FullName__contains=fullname) | Q(ButtonEvent__contains=fullname))
   
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
    """按钮新增和修改"""
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
            roleModel = models.Sys_Button.objects.get(KeyId=keyId)
       except Exception as err:
           roleModel = None       
       if keyId > 0 and roleModel != None:
           return render(request,
                 'adminApp/button/edit.html',{
                     'Model':roleModel,
                     'title':'修改'})
       else:
           return render(request,'adminApp/button/edit.html',{'Model':models.Sys_Button(KeyId=0),'title':'新增'})  
    else :
       form = request.POST
       keyId = int(form["KeyId"])
       Result = False    
       Msg = ""
       try:
          if keyId > 0:
              userBykeyId = models.Sys_Button.objects.filter(KeyId=keyId).first()
              sys_user_form = models.Sys_Button_Form(request.POST,instance=userBykeyId)
              if sys_user_form.is_valid():
                  sys_user_form.save()
                  Result = True  
             
          else:              
              sys_user_form = models.Sys_Button_Form(request.POST)
              if sys_user_form.is_valid():
                  userPost = sys_user_form.save(commit=False) #在sys_user_form.save(commit=False时，添加一些表单中未有的数据)
                  userPost.DateTime = datetime.now()
                  userPost.save()
                  Result = True  
                 
       except Exception as err:
           Result = False 
           Msg = err.args
     
       # 返回Json 数据
       name_dict = {'Result': Result, 'Msg': Msg}
       return JsonResponse(name_dict)

def delete(request,KeyId):
  """删除按钮"""
  use2r = request.session.get(settings.ADMIN_SESSION,default=None)
  if use2r is None:
     return HttpResponseRedirect('/adminlogin')
  Result = False    
  Msg = ""
  try:
         roleModel = models.Sys_Button.objects.filter(KeyId=KeyId).delete()
         Result = True
  except Exception as err:
        Msg = err.args     

  name_dict = {'Result': Result, 'Msg': Msg}
  return JsonResponse(name_dict)