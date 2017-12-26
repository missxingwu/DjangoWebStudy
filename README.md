# DjangoWebStudy
1.0 VS 2017 创建DjangoWeb 项目，Python 环境为共享环境（P.S. 用虚拟环境无法通过桌面GitHub 上传 暂时不知道是什么问题 2017.12.13）

2.0 修改默认连接数据库为MySql 
 
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends,mysql',
             'NAME':'FirstDjango',
             'USER':'root',
             'PASSWORD':'123456',
             'HOST':'127.0.0.1',
             #'PORT':'3306',默认端口
         }
     }

3.0  创建数据 （用命令启动必须要转到项目目录）

     1.0 创建数据 python manage.py makemigrations（检测模型） （不适应Mysql新建数据，用sqllite是可以创建数据库）
     2.0 将生成的py文件应用同步到数据库  python manage.py migrate （数据迁移）
     3.0 创建超级管理员 python manage.py createsuperuser (# 修改 用户密码可以用：python manage.py changepassword username)
     4.0 启动 python manage.py runserver（P.S. VS2017 可以用自带的启动直接开启项目）

4.0 自定义模型 和Url路由规则
     
	 1.0 所有模型继承自models.Model，并且默认都有默认主键,自定义主键时加上primary_key=True，如： KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
	 2.0 添加需要的模型后 更新（ python manage.py makemigrations  python manage.py migrate）先检查在更新到数据库
	 3.0 模型转字典: from django.forms.models import model_to_dict    model_to_dict(models.Sys_User)。字典转模型：models.Sys_User(**back)参考修改密码注释

	 路由规则和asp.net MVC 路由规则基本相似，写路由规则的时候 都是从越精准路由写前面，越模糊路由下后面，它们都是从上往下匹配。列 url配置里：按钮管理

5.0 自定义后台登录页面
    
	1.0 创建后台页面（目前用的是Django 默认用户管理登录2017.12.13），引入静态文件 列：
	  {% load staticfiles %}
      <link rel="icon" href="{% static 'adminApp/Image/monkey-48.ico' %}">
      <link href="{% static 'adminApp/Login/css/login.css' %}" rel="stylesheet" />
	2.0 form 表单数据提交 注意CSRF验证,解决方法 <form>{% csrf_token %}</from>
	3.0 from django.contrib.auth.hashers import make_password, check_password  Django 加密解密，每次生成的密码都是一样的，加密：  make_password(PassWord)，解密：check_password("12", pwd) 明文和明文对比，返回True Or False

6.0 Django Session
 
    1.0 # 创建或修改 session：request.session[key] = value # 获取 session：request.session.get(key,default=None) # 删除 session  del request.session[key] # 不存在时报错
	2.0 Django 当返回 JsonResponse时， 存Session 是要序列化 ，转Json 注意： 不能直接序列化 模型类，解决办法：
	
	    2.1 可以在模型一下自定义一个toJson 方法 参考 模型 Sys_User
		2.0 直接 转为一个集合对象
		2.2 把模型转为一个字典，然后在序列化

	3.0 Session 配置
	     先开启设置，默认是FALSE
         SESSION_SAVE_EVERY_REQUEST=True
         SESSION_EXPIRE_AT_BROWSER_CLOSE=True 关闭浏览器失效 or  SESSION_COOKIE_AGE=60*30  有效时间 30分钟         

7.0 Django 数据库
   
    1.0 获取对象的方法  列： 
	   Sys_User.objects.all() # 查询所有，返回一个列表
       Sys_User.objects.all()[:10] 切片操作，获取10个人，不支持负索引，切片可以节约内存，不支持负索引，后面有相应解决办法，第7条
       Sys_User.objects.get(Account="WeizhongTu") # 名称为 WeizhongTu 的一条，多条会报错，

	   get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter
       Sys_User.objects.filter(Account="abc") # 等于Sys_User.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人
       Sys_User.objects.filter(Account="abc") # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件

	   Sys_User.objects.filter(Account__contains="abc") # 名称中包含 "abc"的人
       Sys_User.objects.filter(Account__icontains="abc") #名称中包含 "abc"，且abc不区分大小写
        
       Sys_User.objects.filter(Account__regex="^abc") # 正则表达式查询
       Sys_User.objects.filter(Account__iregex="^abc")# 正则表达式不区分大小写
        
       # filter是找出满足条件的，当然也有排除符合某条件的
       Sys_User.objects.exclude(Account__contains="WZ") # 排除包含 WZ 的Sys_User对象
       Sys_User.objects.filter(Account__contains="abc").exclude(age=23) # 找出名称含有abc, 但是排除年龄是23岁的

	2.0 创建对象的方法
       # 方法 1
       Sys_User.objects.create(Account="admin", Email="admin@163.com")
        
       # 方法 2
       twz = Sys_User(Account="admin", Email="admin@163.com")
       twz.save()
        
       # 方法 3
       twz = Sys_User()
       twz.Account="admin"
       twz.Email="admin@163.com"
       twz.save()
        
       # 方法 4，首先尝试获取，不存在就创建，可以防止重复
       Sys_User.objects.get_or_create(Account="admin", Email="admin@163.com")

	3.0 更新某个内容

	   3.1 批量更新，适用于 .all()  .filter()  .exclude() 等后面 (危险操作，正式场合操作务必谨慎)
	      Sys_User.objects.filter(Account__contains="abc").update(Account='xxx') # 名称中包含 "abc"的人 都改成 xxx
          Sys_User.objects.all().delete() # 删除所有 Sys_User 记录

	   3.2 单个 object 更新，适合于 .get(), get_or_create(), update_or_create() 等得到的 obj，和新建很类似。
	      twz = Sys_User.objects.get(name="admin")
          twz.Account="admin"
          twz.Email="admin@163.com"
          twz.save()  # 最后不要忘了保存！！！

    4.0 删除符合条件的结果
	  
	  Sys_User.objects.filter(Account__contains="abc").delete() # 删除 名称中包含 "abc"的人 
      如果写成 
      user = Sys_User.objects.filter(Account__contains="abc")
      user.delete()
      效果也是一样的，Django实际只执行一条 SQL 语句。

	5.0 注意事项：

      (1). 如果只是检查 Entry 中是否有对象，应该用 Entry.objects.all().exists()      
      (2). QuerySet 支持切片 Entry.objects.all()[:10] 取出10条，可以节省内存      
      (3). 用 len(es) 可以得到Entry的数量，但是推荐用 Entry.objects.count()来查询数量，后者用的是SQL：SELECT COUNT(*)      
      (4). list(es) 可以强行将 QuerySet 变成 列表

	6.0 排序  Sys_User.objects.all().order_by('Account') # 在 column Account 前加一个负号，可以实现倒序 Sys_User.objects.all().order_by('-Account')

	7.0 其它
	   
	    QuerySet 支持链式查询  Sys_User.objects.filter(Account_contains="a").exclude(email="abc@163.com"),
		不支持负索引 1 使用 reverse() 解决  Sys_User.objects.all().reverse()[:2] # 最后两条,2 使用 order_by 倒序  Sys_User.objects.order_by('-Account')[:20] # id最大的20条。
		使用 .distinct() 去重

8.0 templates 模板

    1.0 显示一个基本的字符串在网页上  {{ title }}，获取当前网址：{{ request.path }}。获取当前 GET 参数：{{ request.GET.urlencode }}。合并到一起用的一个例子：<a href="{{ request.path }}?{{ request.GET.urlencode }}&delete=1">当前网址加参数 </a>

	2.0 for 循环 
	    {% for i in TutorialList %}
          {{ i }}
        {% endfor %}
		在for循环中还有很多有用的东西
		   forloop.counter	索引从 1 开始算
           forloop.counter0	索引从 0 开始算
           forloop.revcounter	索引从最大长度到 1
           forloop.revcounter0	索引从最大长度到 0
           forloop.first	当遍历的元素为第一项时为真
           forloop.last	当遍历的元素为最后一项时为真
           forloop.parentloop  用在嵌套的 for 循环中，获取上一层 for 循环的 forloop

		当列表中可能为空值时用 for  empty
		  <ul>
          {% for athlete in athlete_list %}
              <li>{{ athlete.name }}</li>
          {% empty %}
              <li>抱歉，列表为空</li>
          {% endfor %}
          </ul>

9.0 Django Manager 管理器（待补充）
  
    1.0 添加额外的管理器方法 列：  Sys_Menu 模型里

10.0 序列化

    1.0 返回JSon数据 用 JsonResponse，serializers.serialize("json", models.Sys_User.objects.filter(Account=Account))序列化Django查询处理的数据，会带有 对象名称
    2.0 import json 进行Json 序列化，序列化时间格式会出现问题，解决办法：
    
        class DateEncoder(json.JSONEncoder):  
            def default(self, obj):  
                if isinstance(obj, pydatetime): 
                    return obj.strftime("%Y-%m-%d %H:%M:%S")  
                else:  
                    return json.JSONEncoder.default(self, obj) 
        json.dumps({'date': times,'name':name}, cls = DateEncoder,ensure_ascii=False) ，序列化后字符串会自动被转换为unicode字符串，要想得到字符串的真实表示，需要用到参数ensure_ascii=False(默认为True)。	

 11.0 引入自定义模块
   
    1.0 当要引入的模块和被引入的模块在同一个路径时  可以直接 import
	2.0 当他们不在同目录下是 参考role_list.py 引入 jsonhelp 用：
	        import sys 
			sys.path.append('app/ListTimeToJSon')
			import JsonHelp

12.0 Model + Form 操作
   
    1.0 ModelForm常用组件
	      1.1  class Meta:
                model,                           # 对应Model的
                fields=None,                     # 字段
                exclude=None,                    # 排除字段
                labels=None,                     # 提示信息
                help_texts=None,                 # 帮助提示信息
                widgets=None,                    # 自定义插件
                error_messages=None,             # 自定义错误信息（整体错误信息from django.core.exceptions import NON_FIELD_ERRORS）
                field_classes=None               # 自定义字段类 （也可以自定义字段）
                localized_fields=('birth_date',) # 本地化，如：根据不同时区显示数据
                如：
                    数据库中     
                        2016-12-27 04:10:57
                    setting中的配置
                        TIME_ZONE = 'Asia/Shanghai'
                        USE_TZ = True
                    则显示：
                        2016-12-27 12:10:57
          1.2 验证执行过程
              is_valid -> full_clean -> 钩子 -> 整体错误
          
          1.3 字典字段验证
              def clean_字段名(self):
                  # 可以抛出异常
                  # from django.core.exceptions import ValidationError
                  return "新值"
          1.4 用于验证
              model_form_obj = XXOOModelForm()
              model_form_obj.is_valid()
              model_form_obj.errors.as_json()
              model_form_obj.clean()
              model_form_obj.cleaned_data
          1.5 用于创建
              model_form_obj = XXOOModelForm(request.POST)
              #### 页面显示，并提交 #####
              # 默认保存多对多
                  obj = form.save(commit=True)
              # 不做任何操作，内部定义 save_m2m（用于保存多对多）
                  obj = form.save(commit=False)
                  obj.save()      # 保存单表信息
                  obj.save_m2m()  # 保存关联多对多信息
          
          1.6 用于更新和初始化
              obj = model.tb.objects.get(id=1)
              model_form_obj = XXOOModelForm(request.POST,instance=obj)
              ...
          
              PS: 单纯初始化
                  model_form_obj = XXOOModelForm(initial={...})
		  1.7 save()方法 和 save_m2m()方法，当你的model中含有many-to-many的数据模型，那么你将无法使用save（）方法去保存数据，只能使用save_m2m()方法来保存
		      form = PointRuleForm(request.POST)
              if form.is_valid():
                 point = form.save(commit=False)  #在form.save(commit=False时，添加一些表单中未有的数据)
                 point.Password = "加密密文"  
                 point.save()

13.0 django 事务
    
	django手动配置事务的方式主要有三种：第一种是将一个http request的所有数据库操作包裹在一个transaction中，第二种是通过transaction中间件对http请求的事务拦截，第三种是自己在view中通过装饰器灵活控制事务

	   1.0 第一种 直接在配置文件 DATABASES 中 加上 'ATOMIC_REQUESTS' : True
	   2.0 第二种 配置方法是在settings.py中配置MIDDLEWARE_CLASSES，需要注意的是，这样配置之后，与你中间件的配置顺序是有很大关系的。在 TransactionMiddleware 之后的所有中间件都会受到事务的控制。但CacheMiddleware，UpdateCacheMiddleware，FetchFromCacheMiddleware 这些中间件不会受到影响，因为cache机制有自己的处理方式，用了内部的connection来处理。另外TransactionMiddleware 只对默认的数据库配置有效，如果要对另外的数据连接用这种方式，必须自己实现中间件。（此处必须声明，对于这种方法，本人没有研究过，只是看了一下网上的资料。官网中间件文档链接：https://docs.djangoproject.com/en/2.0/ref/middleware/）

	   3.0 第三种 在view中通过装饰器灵活控制事务
	       
		   1.0 用装饰器 @transaction.atomic

		         @transaction.atomic
                 def rolepost(request):
				   当 里面报错的时候，会自动回滚回去，注意 如果在 try里报错，它是不会回滚。

		   2.0 用 with transaction.atomic(): 用try 包裹起来
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
    
                except :
                    Result = False
		   
		   3.0 回滚到保存点 sid = transaction.savepoint()  transaction.savepoint_commit(sid)  transaction.savepoint_rollback(sid)：

                @transaction.atomic
                def viewfunc(request):
                
                    a.save()
                    # transaction now contains a.save()
                
                    sid = transaction.savepoint()
                
                    b.save()
                    # transaction now contains a.save() and b.save()
                
                    if want_to_keep_b:
                        transaction.savepoint_commit(sid)
                        # open transaction still contains a.save() and b.save()
                    else:
                        transaction.savepoint_rollback(sid)
                        # open transaction now contains only a.save()
			 

14.0 django 图片显示

     在 django 中不像.net 那样有根目录的概念 而取而代之的是包的概念， 通过URLS.PY 来提供每个URL 对应的DJANGO的 函数来显示页面 
　　 在包的 temolates目录中 的html页面里面 是不能直接写图片 或者 CSS JS 文件的 相对|绝对 路径的 ， 而是用 URLS 提供的URL对应 图片/js/css 目录的 
     列：参考 url 和 settings  列子