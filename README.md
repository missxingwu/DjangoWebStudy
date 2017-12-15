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

4.0 自定义模型
     
	 1.0 所有模型继承自models.Model，并且默认都有默认主键,自定义主键时加上primary_key=True，如： KeyId = models.AutoField(primary_key=True,verbose_name="主键ID")
	 2.0 添加需要的模型后 更新（ python manage.py makemigrations  python manage.py migrate）先检查在更新到数据库

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

9.0 Django Manager 管理器
  
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
