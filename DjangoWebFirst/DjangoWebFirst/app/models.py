"""
Definition of models.
"""

from django.db import models
import json
import datetime
from django.forms import ModelForm
  
class UserMenuManager(models.Manager):
    def with_counts(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT distinct a.RoleId,a.UserId as AccountId,d.*
            FROM app_sys_userrole a 
            join app_Sys_Role b on a.RoleId=b.KeyId
            join app_Sys_RoleMenu c on c.RoleId=a.RoleId
            join app_Sys_Menu d on d.KeyId=c.MenuId 
            ORDER BY SortNum """)
       
        
        result_list = []
        for row in cursor.fetchall():
            p = self.model(KeyId=row[2], ParentId=row[3], FullName=row[4],Icon=row[5],NavigateUrl=row[6],IsRoot=row[7],Description=row[8],SortNum=row[9],IsDeleted=row[10],DateTime=row[11])
            p.RoleId = row[0]
            p.AccountId = row[1]
            result_list.append(p)
          
        return result_list


 #按钮表
class Sys_Button(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    FullName = models.CharField(max_length=50,verbose_name="名称")  
    Icon = models.CharField(max_length=30,verbose_name="图标")    
    ButtonEvent = models.CharField(max_length=30,verbose_name="按钮点击事件名称")
    Description = models.TextField(verbose_name="描述")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
    #def __str__(self):
    #    return self.FullName

    class Meta:
        verbose_name = "权限按钮"
        verbose_name_plural = "权限按钮"
     
 #字典表
class Sys_Dictionary(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    ParentId = models.IntegerField(verbose_name="父级")  
    FullName = models.CharField(max_length=50,verbose_name="称呼")    
    Img = models.CharField(max_length=50,verbose_name="图片")
    Url = models.CharField(max_length=50,verbose_name="链接")
    Description = models.TextField(verbose_name="描述")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
    PIds = models.CharField(max_length=50,verbose_name="所有父级")
    class Meta:
        verbose_name = "字典"
        verbose_name_plural = "字典列表"
   
 #错误日志表
class Sys_ErrorLog(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    Title = models.CharField(max_length=50,verbose_name="标题")  
    ErrorMsg = models.CharField(max_length=50,verbose_name="错误详情")       
    DateTime = models.DateTimeField(verbose_name="时间")
    class Meta:
        verbose_name = "日志"
        verbose_name_plural = "日志记录"
  
 #菜单表
class Sys_Menu(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    ParentId = models.IntegerField(verbose_name="父级")
    FullName = models.CharField(max_length=50,verbose_name="称呼")
    Icon = models.CharField(max_length=50,verbose_name="图标") 
    NavigateUrl = models.CharField(max_length=50,verbose_name="菜单链接")  
    IsRoot = models.BooleanField(verbose_name="是否为根菜单")  
    Description = models.TextField(verbose_name="描述")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
    objects = UserMenuManager()
    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = "菜单列表"
  
#菜单表
class Sys_MenuButton(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    MenuId = models.IntegerField(verbose_name="菜单ID")
    ButtonId = models.IntegerField(verbose_name="按钮ID")
    DateTime = models.DateTimeField(verbose_name="时间")
    class Meta:
        verbose_name = "菜单按钮"
        verbose_name_plural = "菜单按钮列表"

#组织架构表
class Sys_Organization(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    ParentId = models.IntegerField(verbose_name="父级ID")
    FullName = models.CharField(max_length=50,verbose_name="名称")
    Phone = models.CharField(max_length=50,verbose_name="组织联系电话")
    Description = models.TextField(verbose_name="地址")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
    PIds = models.CharField(max_length=50,verbose_name="所有父级ID")
    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = "组织架构列表"

       
#角色表
class Sys_Role(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    FullName = models.CharField(max_length=50,verbose_name="名称")    
    Description = models.TextField(verbose_name="描述")
    IsDeleted = models.BooleanField(verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")
    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色列表"





#角色对应菜单表
class Sys_RoleMenu(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    RoleId = models.IntegerField(verbose_name="角色ID")    
    MenuId = models.IntegerField(verbose_name="菜单ID")
    DateTime = models.DateTimeField(verbose_name="时间")
    class Meta:
        verbose_name = "角色对应菜单"
        verbose_name_plural = "角色对应菜单列表"


#角色对应菜单表按钮
class Sys_RoleMenuButton(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    RoleId = models.IntegerField(verbose_name="角色ID")    
    MenuId = models.IntegerField(verbose_name="菜单ID")
    ButtonId = models.IntegerField(verbose_name="按钮ID")
    DateTime = models.DateTimeField(verbose_name="时间")
    class Meta:
        verbose_name = "角色对应菜单按钮"
        verbose_name_plural = "角色对应菜单按钮列表"

#用户表
class Sys_User(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    Account = models.CharField(max_length=50,verbose_name="账号")    
    PassWord = models.CharField(max_length=128,verbose_name="密码")   
    FullName = models.CharField(max_length=50,verbose_name="称呼")   
    Job = models.CharField(max_length=50,verbose_name="职位")  
    Educational = models.CharField(max_length=100,verbose_name="学历")  
    FinishSchool = models.CharField(max_length=100,verbose_name="毕业学校")
    OrgId = models.CharField(max_length=50,verbose_name="所属组织")
    HeadImg = models.CharField(max_length=250,verbose_name="头像")
    Phone = models.CharField(max_length=50,verbose_name="联系方式")
    Email = models.CharField(max_length=50,verbose_name="邮件")
    Sex = models.BooleanField(verbose_name="性别")
    BirthDay = models.DateTimeField(verbose_name="出生日期")  
    IDCard = models.CharField(max_length=50,verbose_name="身份证")
    Address = models.CharField(max_length=150,verbose_name="地址")
    Description = models.TextField(verbose_name="简介")
    SortNum = models.IntegerField(verbose_name="排序")
    IsDeleted = models.BooleanField(default=False, verbose_name="是否删除")
    DateTime = models.DateTimeField(verbose_name="时间")  
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户列表"

    # 添加一个转Json 方法
    def toJSON(self):        
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

    # 转Json 方法 可读性好点 时间格式化了
    def toJSONDateTime(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
    
        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr),datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr),datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
    
        return json.dumps(d)

    def toList(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

#用户对应角色表
class Sys_UserRole(models.Model):
    KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
    RoleId = models.IntegerField(verbose_name="角色ID")    
    UserId = models.IntegerField(verbose_name="用户ID")
    DateTime = models.DateTimeField(verbose_name="时间")
    class Meta:
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色列表"

class Sys_User_Form(ModelForm):  
    class Meta:  
        model = Sys_User  
        fields = "__all__"      #或('FullName','Email','Account') # #验证哪些字段，"__all__"表示所有字段
        exclude = ['KeyId','Educational', 'FinishSchool', 'Job','PassWord','DateTime']          #排除的字段
    #可以抛出异常 def clean_<fieldname>: 
    def clean_Account(self):
        value = self.cleaned_data['Account']
        if value != 'admin':
            return value
        else:
            raise ValidationError("admin：已经存在")

class Sys_Button_Form(ModelForm):  
    class Meta:  
        model = Sys_Button  
        fields = "__all__"      #或('FullName','Email','Account') # #验证哪些字段，"__all__"表示所有字段
        exclude = ['DateTime']          #排除的字段

class Sys_Menu_Form(ModelForm):  
    class Meta:  
        model = Sys_Menu  
        fields = "__all__"      #或('FullName','Email','Account') # #验证哪些字段，"__all__"表示所有字段
        exclude = ['DateTime','NavigateUrl']          #排除的字段
