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
from django.forms.models import model_to_dict
import time
import sys
sys.path.append('app/ListTimeToJSon')

import JsonHelp
from django.db import transaction #事务
def role_list(request):
    fullname = request.GET.get('FullName')    
    columns = models.Sys_Role.objects.all() #models.Sys_Role.objects.filter(IsDeleted=False)
    if fullname != None and fullname != "": 
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


def add_role(request,):
    """角色新增和修改"""
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

def del_role(request,KeyId):
     """删除角色"""
     use2r = request.session.get(settings.ADMIN_SESSION,default=None)
     if use2r is None:
        return HttpResponseRedirect('/adminlogin')
     Result = False    
     Msg = ""
     try:
            roleModel = models.Sys_Role.objects.filter(KeyId=KeyId).delete()
            Result = True
     except Exception as err:
           Msg = err.args     

     name_dict = {'Result': Result, 'Msg': Msg}
     return JsonResponse(name_dict)


def perm_role(request,keyId):
     """分配权限"""
     use2r = request.session.get(settings.ADMIN_SESSION,default=None)
     if use2r is None:
        return HttpResponseRedirect('/adminlogin')
     
      # var list = bll.GetList<Sys_Menu>(item => item.IsDeleted ==
      # false).ToList();
      #   var list2 = bll.GetList<Sys_MenuButton>(item => item.KeyId !=
      #   null).ToList();
      #    var list3 = bll.GetList<Sys_Button>(item => item.IsDeleted ==
      #    false).ToList();


     try:
          menuList = models.Sys_Menu.objects.filter(IsDeleted=False,IsRoot = False)
          rootMenuList = models.Sys_Menu.objects.filter(IsDeleted=False,IsRoot = True)
          menuButtonList = models.Sys_MenuButton.objects.all()
          buttonList = models.Sys_Button.objects.filter(IsDeleted=False)
          return render(request,'adminApp/role_perm.html',{'title':'分配权限','KeyId':keyId,'menuList':menuList,'menuButtonList':menuButtonList,'buttonList':buttonList,'rootMenuList':rootMenuList})  
     except Exception as err:
         return render(request,'adminApp/role_perm.html',{'title':'分配权限','KeyId':keyId})  
    
def permissions(request):
     """获取权限"""
     use2r = request.session.get(settings.ADMIN_SESSION,default=None)
     if use2r is None:
        return HttpResponseRedirect('/adminlogin')
     if request.method == "GET":       
        roleId = request.GET.get("RoleId")
        roleMenuButtonList = models.Sys_RoleMenuButton.objects.filter(RoleId = roleId)
        roleMenuButtonListTarr = []
        roleMenuListTarr = []
        for item in roleMenuButtonList:
            roleMenuButtonListTarr.append(model_to_dict(item))

    
        roleMenuList = models.Sys_RoleMenu.objects.filter(RoleId = roleId)
        for item in roleMenuList:
            roleMenuListTarr.append(model_to_dict(item))

        backList = {"RoleMenuList":roleMenuListTarr,"RoleMenuButtonList":roleMenuButtonListTarr}
        backListJson = json.dumps(backList,cls =JsonHelp.DateEncoder,ensure_ascii=False)
        return JsonResponse(backListJson,safe=False)
     elif request.method == "POST":
        form = request.POST
        menuIds = form["MenuIds"]
        buttonIds = form["ButtonIds"]
        roleId = form["RoleId"]
        if len(menuIds) > 0:
           menuIds = menuIds.replace("m_","")
        if len(buttonIds) > 0:
           buttonIds = buttonIds.replace("m_","").replace("b_","")

        Result = False    
        Msg = ""
        try:
             menuId = menuIds.split(",")
             buttonId = buttonIds.split(",")
             with transaction.atomic():
               role_menu_to_insert = []
               menu_button_to_insert = []
               count = 0
               # 角色菜单
               while count < (len(menuId) - 1):                     
                     role_menu = models.Sys_RoleMenu(MenuId=menuId[count],RoleId=roleId,DateTime=datetime.now())
                     role_menu_to_insert.append(role_menu)
                     count = count + 1
              # 角色菜单按钮
               count = 0
               while count <(len(buttonId) - 1): 
                     item = buttonId[count].split("|")
                     menu_btn = models.Sys_RoleMenuButton(ButtonId=item[0],MenuId=item[1],RoleId=roleId,DateTime=datetime.now())
                     menu_button_to_insert.append(menu_btn)
                     count = count + 1
               
               models.Sys_RoleMenu.objects.filter(RoleId =roleId).delete()
               models.Sys_RoleMenuButton.objects.filter(RoleId =roleId).delete()

               models.Sys_RoleMenu.objects.bulk_create(role_menu_to_insert)
               models.Sys_RoleMenuButton.objects.bulk_create(menu_button_to_insert)
               Result = True    

               
        except Exception as err:
            Result = False
            Msg = err.args
        
        name_dict = {'Result': Result, 'Msg': Msg}
        return JsonResponse(name_dict)