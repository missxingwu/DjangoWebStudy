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
             #'PORT':'3306',默认档口
         }
     }
3.0  创建数据 （用命令启动必须要转到项目目录）

     1.0 创建数据 python manage.py makemigrations （不适应Mysql）
     2.0 将生成的py文件应用同步到数据库  python manage.py migrate （数据迁移）
     3.0 创建超级管理员 python manage.py createsuperuser (# 修改 用户密码可以用：python manage.py changepassword username)
     4.0 启动 python manage.py runserver（P.S. VS2017 可以用自带的启动直接开启项目）
