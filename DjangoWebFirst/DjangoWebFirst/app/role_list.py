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
import json
from django.forms.models import model_to_dict
import time


class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S') 
        else:  
            return json.JSONEncoder.default(self, obj) 



def role_list(request):
    columns = models.Sys_Role.objects.filter(IsDeleted=True)
    articles = models.Sys_Role.objects.filter(IsDeleted=True)

    total = 2                           # 每页最多显示数据量
    totalCount = len(columns)           # 总数据量
    totalPage = int(totalCount / total)# 总页数
    if totalCount % total > 0:
        totalPage+=1
    

    cus_list = models.Sys_Role.objects.filter(IsDeleted=True)

    #total=request.GET.get('PageSize')

    paginator = Paginator(cus_list, total)

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

    strjsonDatalist = serializers.serialize("json",customer, cls = DateEncoder,ensure_ascii=False)  
    # json 序列化后 会自动转为unicode字符串，要想得到字符串的真实表示，需要用到参数ensure_ascii=False(默认为True)
    strjsonTime = json.dumps({'date': datetime.now()}, cls = DateEncoder,ensure_ascii=False)  
    #strjson = json.dumps(model_to_dict(str))

    #-------------------------------------------------------------------------------------------------------------------
    return JsonResponse(name_dict)
