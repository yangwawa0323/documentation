# Flask 入门

## 安装

安装虚拟环境

```shell
shell$　python -m venv venv
```



## 路由

```python
print(app.url_map)
```



![image-20200904112932321](E:\Documents\Flask 入门.assets\image-20200904112932321.png)



## flask-script 命令行插件

```shell
（venv)$ pip install flask-script
```

然后再在主程序中添加下面内容

```python
from flask_script import Manager
manager = Manager(app)
# ...
if __name__ == '__main__':
manager.run()
```

原有的主程序运行将扩展成以下两种```shell```和```runserver```

```shell
E:\ProjectResources\blog\app>python main.py
usage: main.py [-?] {shell,runserver} ...

positional arguments:
  {shell,runserver}
    shell            Runs a Python shell inside Flask application context.
    runserver        Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help         show this help message and exit

(venv) E:\ProjectResources\blog\app>python main.py runserver
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment. 
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 507-080-159
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```



## Debug

![image-20200904110153188](E:\Documents\Flask 入门.assets\image-20200904110153188.png)



![image-20200904110221958](E:\Documents\Flask 入门.assets\image-20200904110221958.png)



![image-20200904110236720](E:\Documents\Flask 入门.assets\image-20200904110236720.png)



## Jinjia2模版

模版中变量输出,将通过 ``{{  }}```格式

```html
<h1>Hello, {{ name }}!</h1>
```

### **render_template** 函数

* 第一个参数为需要渲染的模版
* 后续的都为 `**kwargs` ,可以通过 **key**=*value* 方式传递

```python
from flask import Flask,render_template
# ...
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)  
```

### 模版中变量

* 字典和列表的输出格式，可以采用原有的 python 格式，也可以使用**对象属性**方式

```html
<p>A value from a dictionary: {{ mydict['key'] }}.</p>
<p>A value from a list: {{ mylist[3] }}.</p>
<p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p>
<p>A value from an object's method: {{ myobj.somemethod() }}.</p>
```

* 模版中的变量可以附加各种滤镜 **filter**

```html
Hello, {{ name|capitalize }}
```

* 常用滤镜函数,了解更多，请[参考官网文档](https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters)

 1.  lower

 2.  upper

 3.  capitalize

 4.  trim

 5.  tojson

 6.  pprint

 7.  format

     ```html
     {{ "%s, %s!"|format(greeting, name) }}
     Hello, World!
     {{ "%s, %s!" % (greeting, name) }}
     {{ "{}, {}!".format(greeting, name) }}
     ```

     

### 条件判断控制

* `if ... else` 条件判断

  ```html
  {% if user %}
     Hello, {{ user }}!
  {% else %}
     Hello, Stranger!
  {% endif %}
  ```

  

* `for` 循环

```html
 <ul>
     {% for city, items in users|groupby("city") %}
   <li>{{ city }}
     <ul>
         {% for user in items %}
         <li>{{ user.name }}</li>
         {% endfor %}</ul>
   </li>
     {% endfor %}
</ul>
```



### 模版的继承

在母版中定义可以被替换的块 **block**,  代码以`block <name>`开头以```endblock```收尾

以下是 `base.html`

```html
<html>
<head>
{% block head %}
<title>{% block title %}{% endblock %} - My Application</title>
{% endblock %}
</head>
<body>
{% block body %}
{% endblock %}
</body>
</html>
```

`index.html`延生母版

```html
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
{{ super() }}

<style>
</style>

{% endblock %}
{% block body %}

<h1>Hello, World!</h1>

{% endblock %}
```

> 注意：继承母版中使用到的块将覆盖母版原有的内容，如果仍需要母版中的内容，调用**super()** 函数



#### 使用 bootstrap

可以在模版中使用 bootstrap 前端的框架，Flask自带 `flask-bootstrap`插件扩展

```shell
（venv)$ pip install flask-bootstrap
```

将初始化的app交给Bootstrap

```python
from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app
```

在你自定义的模版中只需要继承母版 `bootstrap/base.html`，在这个母版中定义很多的块，**此母版不需要自己编写**，它取至于`venv\Lib\site-packages\flask_bootstrap\templates\bootstrap\`

```html
{% extends "bootstrap/base.html" %}
{% block title %}Flasky{% endblock %}
{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/">Flasky</a>
    </div>
    <div class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        <li><a href="/">Home</a></li>
      </ul>
    </div>
  </div>
</div>
{% endblock %}

{% block content %}
<div class="container">
  <div class="page-header">
    <h1>Hello, {{ name }}!</h1>
  </div>
</div>
{% endblock %}
```

其中预先定义好的`block`, 请参考[官方文档](https://pythonhosted.org/Flask-Bootstrap/basic-usage.html#available-blocks)

![image-20200910134827720](E:\Documents\Flask 入门.assets\image-20200910134827720.png)

>  上面提及到 `super()`，bootstrap 模版中的 `scripts` *block* 一定要调用此函数，否则会将`jquery.js`和`bootstrap.min.js`覆盖了

```html
{% block scripts %}
{{ super() }}
<script type="text/javascript" src="my-script.js"></script>
{% endblock %}
```

## Web Form 表单

程序中需要提交数据表单

```shell
(venv)$ pip install flask-wtf
```

### 网站 CSRF 请求的防御

用户需要先行请求，获得网站的 `Token` **令牌**，所有提交的表单信息都需要对 `Token` 检测，我们需要提前设置服务器端用于生产`Token`的密钥

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
```

### Form 类

当使用 `flask-wtf`时，每一个表单都由一个继承于**Form**类代表，

```python
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')
```

> `flask_wtf.Form`现已更名`flask_wtf.FlaskForm`

下图中为 Flask-wtf 定义和映射到网页中的字段

![image-20200910170440739](E:\Documents\Flask 入门.assets\image-20200910170440739.png)

下图中为`wtforms.validators`验证的函数器

![image-20200910170643303](E:\Documents\Flask 入门.assets\image-20200910170643303.png)

### 在模版中的渲染

```html
<form method="POST">
	{{ form.name.label }} {{ form.name() }}
	{{ form.submit() }}
</form>

```

如果需要自定义样式，可以在字段函数中添加 `id`

```html
<form method="POST">
	{{ form.name.label }} {{ form.name(id='my-text-field') }}
	{{ form.submit() }}
</form>
```

最简单，直接使用 *flask-bootstrap*中定义 `wtf.quick_form()` 宏命令

```html
{% import "bootstrap/wtf.html" as wtf %}
{{ wtf.quick_form(form) }}
```

### 视图中处理 Form

```python
@app.route('/', methods=['GET', 'POST'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template('index.html', form=form, name=name)
```



## 重定向和报错

### redirect函数

```python
from flask import Flask, render_template, session, redirect, url_for

@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'))
```



### 自定义错误页面

```python
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500
```



## Session

## 弹框消息

1. 视图中使用`flash()`函数堆积消息

```python
from flask import Flask, render_template, session, redirect, url_for, flash
@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
			session['name'] = form.name.data
			form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html',form = form, name = session.get('name'))

```
2. 在模版中循环的将`get_flashed_messages()`中的消息展示出来

```html
{% block content %}
	<div class="container">
  {% for message in get_flashed_messages() %}
	<div class="alert alert-warning">
		<button type="button" class="close" data-dismiss="alert">&times;		</button>
		{{ message }}
	</div>
  {% endfor %}

{% block page_content %}{% endblock %}
	</div>
{% endblock %}
```



## 链接

app.add_url_route()

url_for函数

## 静态文件

**url_for**('**static**', filename='css/styles.css', **_external**=True) 将解析为 *http://localhost:5000/static/css/styles.css*  

## 项目结构

## 应用程序设置

## 数据库访问

支持关系型数据库

* PostgreSQL
* MySQL
* Oracle
* SQLite
* Microsoft SQL Server
* Firebird SyBase

### Migration 数据库迁移和更新

对数据模型的修改，固然可以通过`db.create_all()`和`db.drop_all()`,重建表，但是Flask提供了一个更为好用的插件，可以通过命令的方式对数据库迁移更新，同时保留了升级的记录用以回滚到特定的版本。

首先需要安装

```shell
（venv）$　pip install flask-migrate

```



在 app.py 中

```python
from flask_migrate import Migrate, MigrateCommand
from flask_scripts import Manager, Shell
# ...
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# ...
manager.run()
```



### many-to-many  关系

实现多对多关系，不能再建立数据模型，只能建立一个存放建联关系的中间表

如图

![image-20200904161914087](E:\Documents\Flask 入门.assets\image-20200904161914087.png)

```python
import datetime, re
from app import db

def slugify(s):
	return re.sub('[^\w]+', '-', s).lower()

entry_tags = db.Table('entry_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),   # tag lowcase
	db.Column('entry_id', db.Integer, db.ForeignKey('entry.id')) # entry lowcase
	)
# all tables in database are lowcase

class Entry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	slug = db.Column(db.String(100), unique=True)
	body = db.Column(db.Text)
	created_timestamp = db.Column(db.DateTime,
	default=datetime.datetime.now)
	modified_timestamp = db.Column(
		db.DateTime,
		default=datetime.datetime.now,
		onupdate=datetime.datetime.now)
	tags = db.relationship('Tag', secondary=entry_tags,
	backref=db.backref('entries', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
		self.generate_slug()

    def generate_slug(self):
		self.slug = ''
		if self.title:
			self.slug = slugify(self.title)

    def __repr__(self):
		return '<Entry %s>' % self.title

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	slug = db.Column(db.String(64), unique=True)
	
    def __init__(self, *args, **kwargs):
		super(Tag, self).__init__(*args, **kwargs)
		self.slug = slugify(self.name)

    def __repr__(self):
		return '<Tag %s>' % self.name
```

上述代码中其中 7 -  10 行， 直接中SQLAlchemy建立一个存放建联关系的中间表

```python
entry_tags = db.Table('entry_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
	)
```

而在其中一个数据模型中，如上Entry中

```python
	tags = db.relationship('Tag', secondary=entry_tags,
	backref=db.backref('entries', lazy='dynamic'))
```

Entry 加入新的属性 `tags`, 是由 **db.relationship**函数返回值

* 其中第1，2个参数代表，告知 SQLAlchemy 通过 `entry_tags` 表查询`Tag`模型数据

* 第三个参数 **backref** 很关键，它建立了一个 **回参（back-reference)** ,可以让我们从`Tag`模型中反向的关联一系列的`Entry`

  > 注意，`Tag`模型中没有再次建立db.relationship,通过回参注入了一个新的属性
  >
  > db.backref中的第二个参数 lazy='dynamic', 让SQLAlchemy查询时才获取数据，而不是装载所有的Entry。



## Blueprint 蓝图

## 命令行接口

## Live reload 调试

每次修改代码或者模版都需要杀死终端，然后重新运行 flask，可以安装 `python-livereload` 实现即使刷新

```shell
(venv) pip install livereload
```

而 Flask 中 main.py 代码修改如下

```python
from app import app

# live reload
from livereload import Server

import views

if __name__ == '__main__':
    # app.run()  # Flask app
    
    # live reload server
    server = Server(app.wsgi_app)
    server.serve() # by default listenning on 127.0.0.1:5500
    # server.server(port="5000", host="0.0.0.0")
```



由于版本出现的问题，如果修改代码后出现下面的报错

```shell
      ...
      File "e:\ProjectResources\blog\venv\lib\site-packages\tornado\platform\asyncio.py", line 90, in close
        self.asyncio_loop.close()
      File "E:\Python38\lib\asyncio\selector_events.py", line 89, in close
        raise RuntimeError("Cannot close a running event loop")
    RuntimeError: Cannot close a running event loop
```

可以将 **tornado\platform\asyncio.py** 的 *self.asyncio_loop.close()* 第90行暂时注释



##  官方参考文档

* [Flask 1.1](https://flask.palletsprojects.com/en/1.1.x/)
* [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [flask-bootstrap](https://pythonhosted.org/Flask-Bootstrap/index.html)
* [bootstrap 3.4](https://getbootstrap.com/docs/3.4/css/)
* [SQLAlchemy](https://docs.sqlalchemy.org/en/13/)
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
* [Vue 2.0](https://cn.vuejs.org/v2/guide/)
* [Jquery API](https://api.jquery.com/)

