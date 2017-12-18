from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password #加密解密
from django.core import serializers
from app import models
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #分页
import json
from django.forms.models import model_to_dict
import time
import sys
sys.path.append('app/ListTimeToJSon')

import JsonHelp

def role_list(request):
    fullname = request.GET.get('FullName')    
    columns = models.Sys_Role.objects.filter(IsDeleted=False)
    if fullname != None: 
      columns = models.Sys_Role.objects.filter(IsDeleted=False,FullName__contains=fullname)

    total = int(request.GET.get('PageSize')) # 每页最多显示数据量
    if total <= 0:
        total = 2

    totalCount = len(columns)                # 总数据量
    totalPage = int(totalCount / total)      # 总页数
    if totalCount % total > 0:
        totalPage+=1
    
    
    paginator = Paginator(columns, total)

    page = request.GET.get('PageIndex')
   
    #if page:
     #   article_list = paginator.page(page).object_list
    #else:
     #   article_list = paginator.page(1).object_list
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)

    #return render(request, 'index.html', {'cus_list': customer,
    #'columns':columns, 'articles': article_list})


    result_list = []
    for row in customer.object_list:
        rowJson = {"FullName":row.FullName,"Description":row.Description,"CreateDate":row.DateTime,"KeyId":row.KeyId}
        result_list.append(rowJson)
    
  
    name_dict = {"rows": result_list, "total": total,"totalCount":totalCount,"totalPage":totalPage}

    #---------------------------------------------------Json 序列化学习
    #varda =time.strftime('%Y-%m-%d %H:%M:%S',str.DateTime) 把时间序列化为Json 格式

    strjsonDatalist = serializers.serialize("json",customer, cls = JsonHelp.DateEncoder,ensure_ascii=False)  
    # json 序列化后 会自动转为unicode字符串，要想得到字符串的真实表示，需要用到参数ensure_ascii=False(默认为True)
    strjsonTime = json.dumps({'date': datetime.now()}, cls = JsonHelp.DateEncoder,ensure_ascii=False)  
    #strjson = json.dumps(model_to_dict(str))

    #-------------------------------------------------------------------------------------------------------------------
    return JsonResponse(name_dict)

def add_role(request):
    """Renders the role_add page."""
    #assert isinstance(request, HttpRequest)
    use2r = request.session.get(settings.ADMIN_SESSION,default=None)
    keyId = 0
    try:
         keyId = int(request.GET.get('KeyId'))
    except Exception as err:
          keyId = 0    
          
    if request.method == "GET":
       try:
            roleModel = models.Sys_Role.objects.get(KeyId=keyId)
       except Exception as err:
           roleModel = None       
       if keyId > 0 and roleModel != None:
           return render(request,
                 'adminApp/role_add.html',{
                     'model':roleModel,
                     'title':'修改'})
       else:
           return render(request,'adminApp/role_add.html',{'model':'add','title':'新增'})  
    else :
       form = request.POST
       keyId = int(form["KeyId"])
       fullname = form["FullName"]
       description = form["Description"]
       Result = False    
       Msg = ""
       try:
            ro = models.Sys_Role(FullName=fullname,Description=description,IsDeleted=False,DateTime=datetime.now())
            if keyId > 0:
                ro.KeyId = keyId
          
            ro.save()
            Result = True  
       except Exception as err:
           Result = False 
           Msg = err.args
     
       # 返回Json 数据
       name_dict = {'Result': Result, 'Msg': Msg}
       return JsonResponse(name_dict)
