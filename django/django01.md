# Django Day01

## 优点
1.重量级(功能齐全)
2.安全性高(XSS攻击，Session劫持...)
3.后台存储数据库，可以多元化的，MySQL,Oracle...,
4.纯Python
5.MVC方式编程.(Model, View, Controller)
    Model --> Table
    View --> Presentation
    Controller --> Logical

# 安装, 1.8.19
1.下载安装tar包
2.解压
3.进入目录夹
4.python setup.py install
5.测试模块的安装

```python
import django
print django.get_version()
```

# 创建项目目录夹
1.启动一个大型项目
```shell
django-admin startproject mysite
```

mysite
    |__ manage.py  雷同于 **django-admin**
    |__ mysite
          |__ settings.py **全局配置文件**
          |__ urls.py  **网址的规划**

2.采用默认数据库引擎
    1.sqlite数据库
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db50.sqlite3'),
    }
}
```
假设设置好了数据库引擎,我们将要填充 Django 所需要的表
```shell
    python ./manager.py **migrate**
```
一旦改变数据库的服务器的信息,比如将数据库指定到cxk的服务器,我们需要**迁移**


3. 数据建模
建模
   * 反应到数据库中,因为数据存放在此
``` shell
    manage.py startapp polls
```
   * 反应到内存中,python class, 
      * 编写基础类
      * 提交所做变化到数据库中
``` shell
    manage.py makemigrations
    manage.py migrate
```
4.激活APP(仅仅一次)
INSTALLED_APPS = []

5.改变数据库的指向,就需要**迁移一下**数据

项目目录夹的配置文件夹下面全局配置文件
mysite
   |___ mysite
           |___ settings.python

```python
DATABASES = {
    'original': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db50.sqlite3'),
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django50',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'redhat',
    }
}
```


```shell
    manage.py migrate
```

    解决 libmysqlclient.so.18库文件不存在的问题
    ```shell
    sudo -H pip uninstall mysqlclient

    sudo -H pip install --no-binary mysqlclient mysqlclient
    ```

## 建模映射到数据库之间的关系

models.py 转成我们制定的引擎数据库中的表
> 命名规则 app_class(全小写)

```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
```

假设我们APP名称叫做polls,那么将会迁移到数据库中,形成一张polls_student表,也会自动添加一列(主键id)
```sql
CREATE TABLE `polls_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4
```