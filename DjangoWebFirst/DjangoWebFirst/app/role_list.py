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


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)

def datetime_handler(obj):
   if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
   raise TypeError("Type %s not serializable" % type(obj))

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
    totalPage = 3 #totalCount / total # 总页数

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
    str = models.Sys_Role()
    str.FullName = "12321"
    str.KeyId = 1
    str.DateTime = datetime.now()
    #varda =time.strftime('%Y-%m-%d %H:%M:%S',str.DateTime)  把时间序列化为Json 格式
    strjson = json.dumps(str,cls = DateEncoder)  
    strjsonTime = json.dumps({'date': datetime.datetime.now()}, cls = DateEncoder)  
    #strjson = json.dumps(model_to_dict(str))


    for row in customer.object_list:
        #aa = serializers.serialize("json",row)
        rowslist = json.dumps(model_to_dict(row)) 

    return JsonResponse(name_dict)
