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