# Django Day03

## MVC Viewer Presentation
+ 美工的职责，前端负责的部分
  
## 规划网站的地址　sitemap
+ 首页
+ 搜索
+ 关于我们

## 第一个 View
编辑　polls/views.py

> 就是函数，但是它的一个参数总是为用户的请求对象

1. 用户请求
2. django 内部检查网址的合法性
3. 如果合法，我们找对应的视图函数
4. 将视图函数返回的结果回给用户

> django 为了方便管理我们 url, 它采用在每个单独APP目录下放置 urls.py, 然后包含到总的配置文件的 urls.py中来

+ app/urls.py

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

+ project/project/urls.py

```python
  urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
```

> 重点就在 url() 函数
> + 第一个参数就是正则表达式，符合这个表达式的，就去第二个参数
> + 第二个函数就是视图函数，换一句话说，如何显示信息给用户。
>　返回的数据最终是传递给客户的浏览器接收，浏览器识别的是ＨＴＭＬ，所以要把渲染的内容放置ＨＴＭＬ标签中

1. 页面不好看
2. 美工要修改，视图函数要随之修改,硬编码
3. MVC分离


## 渲染
```python
def sayhello(request):
    ''' request: django.http.HttpRequest instance'''
    return render(request, 'polls/index.html')
```

render有三个参数
+ 第一个参数是用户的请求，也就是视图函数的第一个参数
+ 第二个参数，就是模板文件放哪里
> django 有着自己规范的名称空间 APP/templates,我们的模板路径就是相对路径。
+ 第三个参数（一般是一个字典），它代表我们传给美工处理的数据，以后视图函数不会因为非逻辑（显示效果）而修改
  - 字典
  - 取key
  - 取不到 key,Django 自带异常的 KeyError 处理
  - 多出的 key
