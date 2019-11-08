# Django Day04

## 静态文件的访问
+ 脚本
  - <script src="././././"></script>
+ CSS样式表
  - <link rel="stylesheet" href="././././.">
+ 图片资源
  - <img src="./././././">
  
> Django会认为一切URL资源都要合法性，换句话就是定义在urls.py.
> 静态文件用一个统一的目录夹放在APP下，以后还可以收集在一起

1. 需要全局配置中设置 INSTALLED_APPS中添加django.contrib.staticfiles
2. 在自己APP如同模板一样的建立 static 目录
3. 在美工的页面文档上凡是要用静态资源的时候全部采用下面的格式

``` text
    <script src="{% static '././././' %}"></script>
    <img src="{% static './././././.' %}"/>
```

## 模板的继承
1. 建立母版，将未来其他网页有差异的部分抠成**{% block 名字}**
2. 相同部分将会在所有的页面统一的显示
3. 在子页面中
   1. {% extends 'xxx.html '%}
   2. {% block 名字 %} {% endblock %}中的内容替换掉

## 防死链
> Django 利用了一种反向的解析方式来实现无死链
> 在模板中用 {% url 'name' %}
> **name** 也就是我们之前在 APP 下的 urls.py 中**url**函数定义的而且是唯一的参数（第三个）
> 我们就可以通过名字反向生成链接的地址，不用考虑日后如何修改 urls.py