"""
Definition of models.
"""

from django.db import models
   
 #按钮表
class Sys_Button(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    FullName = models.CharField(max_length=50,verbose_name="名称")  
    Icon = models.CharField(max_length=30,verbose_name="图标")    
    ButtonEvent = models.CharField(max_length=30,verbose_name="按钮点击事件名称")
    Description = models.CharField(max_length=30,verbose_name="描述")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
    #def __str__(self):
    #    return self.FullName
     
 #按钮表
class Sys_Dictionary(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    ParentId = models.CharField(max_length=50,verbose_name="父级")  
    FullName = models.CharField(max_length=50,verbose_name="称呼")    
    Img = models.CharField(max_length=50,verbose_name="图片")
    Url = models.CharField(max_length=50,verbose_name="链接")
    Description = models.CharField(max_length=50,verbose_name="描述")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
    PIds = models.CharField(max_length=50,verbose_name="所有父级")  
   
 #错误日志表
class Sys_ErrorLog(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    Title = models.CharField(max_length=50,verbose_name="标题")  
    ErrorMsg = models.CharField(max_length=50,verbose_name="错误详情")       
    DateTime = models.DateTimeField(verbose_name="时间")
  
 #菜单表
class Sys_Menu(models.Model):
    KeyId =models.AutoField(primary_key=True,verbose_name="主键ID")
    ParentId = models.CharField(max_length=50,verbose_name="父级")
    FullName = models.CharField(max_length=50,verbose_name="称呼")
    Icon = models.CharField(max_length=50,verbose_name="图标") 
    NavigateUrl = models.CharField(max_length=50,verbose_name="菜单链接")  
    IsRoot = models.BooleanField(verbose_name="是否为根菜单")  
    Description = models.CharField(max_length=50,verbose_name="描述")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
  
#菜单表
class Sys_MenuButton(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    MenuId = models.CharField(max_length=50,verbose_name="菜单ID")
    ButtonId = models.CharField(max_length=50,verbose_name="按钮ID")
    DateTime = models.DateTimeField(verbose_name="时间")

#组织架构表
class Sys_Organization(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    ParentId = models.CharField(max_length=50,verbose_name="父级ID")
    FullName = models.CharField(max_length=50,verbose_name="名称")
    Phone = models.CharField(max_length=50,verbose_name="组织联系电话")
    Description = models.CharField(max_length=50,verbose_name="地址")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
    PIds = models.CharField(max_length=50,verbose_name="所有父级ID")

       
#角色表
class Sys_Role(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    FullName = models.CharField(max_length=50,verbose_name="名称")    
    Description = models.CharField(max_length=50,verbose_name="描述")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")  


#角色对应菜单表
class Sys_RoleMenu(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    RoleId  = models.CharField(max_length=50,verbose_name="角色ID")    
    MenuId  = models.CharField(max_length=50,verbose_name="菜单ID")
    DateTime = models.DateTimeField(verbose_name="时间")  


#角色对应菜单表
class Sys_RoleMenuButton(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    RoleId  = models.CharField(max_length=50,verbose_name="角色ID")    
    MenuId  = models.CharField(max_length=50,verbose_name="菜单ID")
    ButtonId = models.CharField(max_length=50,verbose_name="按钮ID")
    DateTime = models.DateTimeField(verbose_name="时间")  

#用户表
class Sys_User(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    Account  = models.CharField(max_length=50,verbose_name="账号")    
    PassWord  = models.CharField(max_length=50,verbose_name="密码")   
    FullName = models.CharField(max_length=50,verbose_name="称呼")   
    Job=models.CharField(max_length=50,verbose_name="职位")  
    Educational=models.CharField(max_length=50,verbose_name="学历")  
    FinishSchool=models.CharField(max_length=50,verbose_name="毕业学校")
    OrgId=models.CharField(max_length=50,verbose_name="所属组织")
    HeadImg=models.CharField(max_length=50,verbose_name="头像")
    Phone=models.CharField(max_length=50,verbose_name="联系方式")
    Email=models.CharField(max_length=50,verbose_name="邮件")
    Sex=models.BooleanField(verbose_name="性别")
    BirthDay = models.DateTimeField(verbose_name="出生日期")  
    IDCard=models.CharField(max_length=50,verbose_name="身份证")
    Address=models.CharField(max_length=50,verbose_name="地址")
    Description=models.CharField(max_length=250,verbose_name="简介")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")  
