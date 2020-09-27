# Flask 入门

## 安装

安装虚拟环境,这样所安装的Python三方库就不会因为版本冲突，也不会乱七八糟的不容易管理，**建议每个项目都创建自己的虚拟环境**

```shell
shell$　python -m venv venv
```

激活虚拟环境

```shell
venv\Scripts\activate.bat
```

然后使用虚拟环境下的`pip`安装Flask

```shell
pip install flask
```



## 路由

Flask 是基于最为短小精干的 Werkzeug 的web框架，个人认为最主要的三个核心部分为路由，模版，和数据库交互。其中路由选择可以快速的映射成对用户请求的响应函数。

路由由一个极为方便的装饰器 `@app.route`定义

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/about')
def about_me():
    return 'Our company ...'
```

### 带参数的URL,变量规则

```python
from markupsafe import escape

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

```

参数类型写在"<>"中，有以下五种：

* string: 缺省类型
* int: 正整数
* float: 正浮点值
* path: 和`string`相同，不过它接受 `/`反斜杠
* uuid: `uuid` 格式字符串



```python
print(app.url_map)
```



![标准程序编写调用流程](./Flask 入门.assets/image-20200904112932321.png)



## 启用 Flask APP

两种方式运行 Flask

1. 设置环境变量 `FLASK_APP`,然后调用 `flask run`

```shell
$ export FLASK_APP=hello.py
$ flask run
* Running on http://127.0.0.1:5000/
```

> Windows 下 `set FLASK_APP=hello.py`

2. 直接运行     

```shell
python -m flask run
```

> `create_app(config)`为Factory工厂函数，它是缺省 `flask run` 的入口



## Flask 配置

而生成私钥可以通过下面语句实现

```shell
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
```



## Flask 全局变量

Flask环境下四个全局变量，不用引用即可调用

* **current_app**：应用程序上下文

```python
  >>> from hello import app
  >>> from flask import current_app
  >>> current_app.name
  Traceback (most recent call last):
  ...
  RuntimeError: working outside of application context
  >>> app_ctx = app.app_context()
  >>> app_ctx.push()
  >>> current_app.name
  'hello'
  >>> app_ctx.pop()
```

  

* **g**： 应用程序上下文

* **request**： 请求上下文

* **session**： 请求上下文



## 请求的钩子

* **before_first_request**:　在第一请求时注册钩子函数
* **before_request**：每个请求之前
* **after_request**： 注册一个函数在每个请求之后，只有不出现未处理的异常的情况下
* **teardown_request**：与`after_request`相同，不过无论是否出现异常

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

![image-20200904110153188](./Flask 入门.assets/image-20200904110153188.png)





![image-20200904110221958](./Flask 入门.assets/image-20200904110221958.png)



![image-20200904110236720](./Flask 入门.assets/image-20200904110236720.png)



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

​     

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



### 使用 bootstrap

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

![image-20200910134827720](./Flask 入门.assets/image-20200910134827720.png)

>  上面提及到 `super()`，bootstrap 模版中的 `scripts` *block* 一定要调用此函数，否则会将`jquery.js`和`bootstrap.min.js`覆盖了

```html
{% block scripts %}
{{ super() }}
<script type="text/javascript" src="my-script.js"></script>
{% endblock %}
```



### 自定义模版组件

如果需要定义前端插件保持网站一致性，可以生成网页在其中通过 `macro`块定义，如同定义一个函数一般,甚至可以提供默认值

```html
<!-- forms.html //-->
{% macro input(name, value='', type='text') -%}
    <input type="{{ type }}" value="{{ value|e }}" name="{{ name }}">
{%- endmacro %}

{%- macro textarea(name, value='', rows=10, cols=40) -%}
    <textarea name="{{ name }}" rows="{{ rows }}" cols="{{ cols
        }}">{{ value|e }}</textarea>
{%- endmacro %}
```

 而在其他模版中需要使用上面定义到的表单元器件，两步完成，先导入，再提供变量

```html
{% import 'forms.html' as forms %}
<dl>
    <dt>Username</dt>
    <dd>{{ forms.input('username') }}</dd>
    <dt>Password</dt>
    <dd>{{ forms.input('password', type='password') }}</dd>
</dl>
<p>{{ forms.textarea('comment') }}</p>
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

![image-20200910170440739](./Flask 入门.assets/image-20200910170440739.png)

下图中为`wtforms.validators`验证的函数器

![image-20200910170643303](./Flask 入门.assets/image-20200910170643303.png)

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

验证表单数据可以通过 `validate_on_submit`函数来检测

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



### CSRF 请求的保护

为防止跨域或者编写程序通过保存网页提交数据攻击行为的保护，`Cross site request forgery`, 我们需要启动CSRF检测，也就是在服务器上针对用户的每个请求根据自己的私钥生成表单的隐藏字段，用户提交数据时对Token验证，这样其他服务器伪装提交过来的数据就无法通过验证，这种方式对数据的真实性做保证。

首先，启用 `flask_wtf.csrf.CSRFProtect`

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

> 缺省情况它使用 Flask 配置中的 **SECRET_KEY**, 也可以配置一个**WTF_CSRF_SECRET_KEY** 让其使用额外的密钥生成 `Token`

接着，再在模板中表单中使用

```html
<form method="post">
    {{ form.csrf_token }}
</form>

```

如果没有使用`FlaskForm`类生成表单，则可以通过 `csrf_token()` 函数手工实现

```html
<form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
</form>
```

如果前后端分离模式编程，可以在Javascript脚本中调用 `csrf_token()` 函数，下面给一个Jquery的范例

```javascript
<script type="text/javascript">
    var csrf_token = "{{ csrf_token() }}";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
</script>
```

如果要在视图函数中生成 `token`,则可以通过`flask_wrf.csf.generate_csrf`函数，它**只能放在视图函数中**调用

```python
from flask_wtf.csrf import CSRFProtect, generate_csrf
#...

@app.route('/testform', methods=['GET', 'POST'])
def testForm():
    form = EntryForm()
    token = generate_csrf()
    resp = make_response(render_template('testform.html', form=form))
    resp.headers['X-TOKEN'] = token
    return resp
```

一旦启用 CSRF 保护，所有FlaskForm函数在渲染的时候都会添加 `token`,如果想将某些视图排除在外，可以通过装饰函数 `@csrf.exempt`

```python
@app.route('/foo', methods=('GET', 'POST'))
@csrf.exempt
def my_handler():
    # ...
    return 'ok'
```

甚至可以排除整个`蓝图`下的视图, 请参考下方[蓝图知识点](#blueprint)

```python
csrf.exempt(account_blueprint)
```



更多详情请参考[官方文档](https://flask-wtf.readthedocs.io/en/stable/csrf.html?highlight=csrf#module-flask_wtf.csrf)



## 访问请求的数据

### Request 对象

Request 对象为全局对象，直接从模块中引用即可

```python
from flask import request
```

* 用户的请求，通过 **request.method** 属性获得，其为一个`字符串`

* 用户提交的表单数据，通过 **request.form** 属性获得，其为一个`OrderDict`, 获取不到指定的Key，会出现 `keyError`异常,如果你不认为处理异常，将会出现 `HTTP 400 Bad Request`作为服务器给客户端浏览器的响应 

```python
  @app.route('/login', methods=['POST', 'GET'])
  def login():
      error = None
      if request.method == 'POST':
          if valid_login(request.form['username'],
                         request.form['password']):
              return log_the_user_in(request.form['username'])
          else:
              error = 'Invalid username/password'
      # the code below is executed if the request method
      # was GET or the credentials were invalid
      return render_template('login.html', error=error)
```

  

* 如果用户使用浏览器地址传参数的方式，则要通过 **request.args** 属性获得，其也为一个 `OrderDict`

```python
  searchword = request.args.get('key', '')
```

### 文件上传

文件上传非常简单，首先表单编写需要 `enctype="multipart/form-data"` 属性，接着通过 `request.files`属性获得,然后通过 `save`函数保存到绝对路径下

```python
from flask import request

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
    ...
```

你可以通过 request.files['*xxxx*'].**filename** 属性来保存文件，但容易受到客户端恶意行为攻击，最佳的方法对文件名再做一个处理,下面的例子展示了 `werkzeug.utils.secure_filename` 函数的作用

```python
from flask import request
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))
    ...
```

请参考[详细的范例](https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#uploading-files)，其中对上传的文件存放位置配置以及上传文件的后缀做了限制

### Session

Session用于保持用户与服务器通信过程中的会话数据，设置时直接通过字典形式对 `Key` 赋值，而清空则用 `pop`函数

```python
from flask import Flask, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
```



### 重定向和报错

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

## Response 对请求的回应 

Flask 处理用户的请求，采用下面的步骤作为响应

1. 如果返回存在一个正确类型的 response 对象，那么将直接从 View 函数中返回
2. 如果是一个**字符串**，将创建一个 response 对象以字符串作为数据配以默认参数
3. 如果是一个**dict**, response 对象将使用 jsonify函数创建
4. 如果是一个**tuple**, 满足一下几种格式 `(response, status)`, `(response, headers)`, 或者 `(response, status, headers)`，status将覆盖响应的状态，而headers将作为列表形式追加到头部信息
5. 如果以上都不满足，Flask假设返回的是一个 WSGI 应用并尝试将其转化成 response 对象

如果你想在最终响应处理之后，获得 response 对象，可以通过 `make_response`函数获得，并可以修改它cd 

```python
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-token'] = 'A value'
    return resp
```



## API 和 JSON

根据上面的第三条原则，如果视图函数直接返回 `dict`,将会将其转变成 JSON 格式

```python
@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }
```

也可以通过 `jsonify`将对象序列化

```python
@app.route("/users")
def users_api():
    users = get_all_users()
    return jsonify([user.to_json() for user in users])
```



## 链接

app.add_url_route()

url_for函数



## 静态文件

关于静态文件存放位置，默认在 app 下建立 `static` 目录，也可以通过

```python
app = Flask(__name__, static_url_path='/static/v2')
```

在 Flask 实例化附带 `static_url_path` 参数

而在模版中调用

**url_for**('**static**', filename='css/styles.css', **_external**=True) 将解析为 *http://localhost:5000/static/css/styles.css*  

```html
{% block head %}
{{ super() }}
	<link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
type="image/x-icon">
	<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
type="image/x-icon">
{% endblock %}
```





## 项目结构

### 大型项目开发的文件目录结构

|-**flasky**
	|-**app**/
		|-**templates**/					# 模版文件
		|-**static**/							# 静态文件
		|-**main**/							 # 每个单独子功能建立的目录
			|-\_\_init\_\_.py
			|-errors.py
			|-forms.py
			|-views.py
		|-\_\_init\_\_.py
		|-email.py
		|-models.py
		|-**migrations**/				# 存放Flask-migrate 数据库迁移升级生成的文件
		|-**tests**/							# 测试程序
			|-\_\_init\_\_.py
			|-test*.py
		|-***venv**/							# Python 虚拟环境
	|-requirements.txt  
	|-config.py
	|-manage.py  



### 设计思路

1. config.py 中定义一个Config对象，基于这个对象为父类生成额外不同的配置子类。然后通过字典 `Key` 对应这些类名称

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
   SQLALCHEMY_TRACK_MODIFICATIONS = False

   @staticmethod
   def init_app(app):
       pass


class DevelopmentConfig(Config):
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
       os.path.join(os.path.dirname(__file__), 'demo.db')
   DEBUG = True
   pass


class TestingConfig(Config):
   SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
   pass


config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'default': DevelopmentConfig,
}
```


2.  主程序目录的`app.__init__.py` 前段为各个插件的实例化(**不是初始化**)，然后定义一个`create_app`或者`make_app`这两个工厂函数中的任意一个作为入口。在此函数中对初始化的插件此时对Flask初始化。

```python
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
   app = Flask(__name__)
   app.config.from_object(config[config_name])
   config[config_name].init_app(app)

   bootstrap.init_app(app)
   db.init_app(app)

   from .main import main as main_bluepoint

   app.register_blueprint(main_bluepoint)

   return app

```

   > 17 - 19 行对蓝图的注册和引用，结合后面示例

3. 在主程序下建立子程序目录，在目录的初始化文件`__init__.py`文件中定义蓝图。

```python
from flask import Blueprint

main = Blueprint('main', __name__)

if True:
   from . import views
```

> 注意：一定要先定义蓝图，再引用视图，避免交叉循环引用报错
>
> app/main/\_\_init\_\_.py 引用 app/main/views.py
>
> ```python
> from . import views
> ```
>
> 而 app/main/views.py 又引用 app/main
>
> ```python
> from . import main
> 
> @main.route('/hello')
> def say_hello():
>     return "Hello world!"
> ```
>
> 如果你是使用VS code之类的可视化编程工具，安装了pylint, autopep8 之后, 编辑器会将 ```from...import...```语句自动的提升到`import...`之前，就会造成`__init__.py`从上至下初始化发觉要引用`views.py`，而`views.py`却要引用`main\__init__.py`。但如果先行将蓝图初始化再去调用`views.py`时，此时蓝图已经存在，所以一切正常。为了不让编辑器做出以上行为，我们可以在外面套娃一层`if True`

4. 项目的顶层目录创建启动管理脚本`manage.py`,此时可以向工厂函数`create_app`传递需要使用何种配置启动的`Key`

```python
#!/usr/bin/env python
import os
from app import create_app, db

# from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)

# manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

5. 作为建模都写入`app/models.py`下

```python
from app import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    pass
```

6. 视图文件中都以相对路径形式调用 , 比如`app/main/views.py`

```python
from . import main
from .forms import NameForm
from .. import db
from ..models import User

# ...
```

### 应用程序设置

使用单一程序运行有其弊端，建议使用工厂函数的方式创建应用程序，可以让其传递不同的配置（通过环境变量）来创建程序，这在测试中非常方便。Flask具有者`create_app`默认入口程序，在它之前可以执行各种扩展插件的初始化工作，而在`create_app`中则通过`init_app`函数将插件衔接过来。下面是一个典型的例子

```python
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
#	 attach routes and custom error pages here
	return app
```







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



## [Blueprint 蓝图](#blueprint)

蓝图可以想象成大型施工工地的施工图纸，不同的图纸标注的不同建筑如何施工，所有的图纸加在一起构成大型项目，施工可以分开按图纸施工。

蓝图的创建,比如写入 `app/main/__init__.py`，由于写在目录下的初始化文件中，只要 `import main`将自动调用

```python
from flask import Blueprint
main = Blueprint('main', __name__)

from . import views, errors
```

而视图文件 `app/main/views.py`内容如下

```python
from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		# ...
		return redirect(url_for('.index'))
	return render_template('index.html',
                form=form, name=session.get('name'),
				known=session.get('known', False),
				current_time=datetime.utcnow())
```



> 注意第三行,`from . import main`，由于main的一个目录所以将调用其下`__init__.py`初始化



蓝图也是一样，你可以交由不同的小组开发子模块，子模块中如何路由，如果处理用户的请求。最终合成的时候，只要对蓝图注册到程序中即可（通过`register_blueprint`）。一般写在工厂函数内部注册



```python
def create_app(config_name):
	# ...
	from main import main as main_blueprint
	app.register_blueprint(main_blueprint)
    
	return app
```



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



## SQLAlchemy数据库的操作

### 数据类型

![image-20200914224011594](./Flask 入门.assets/image-20200914224011594.png)

### 逻辑非与或

`from sqlalchemy import or_, and_,not_`

```python
from app.models import User
from app import db

yk = User(username='yangwawa',name='yAnGwAwA0323', email='yangwawa0323@163.com')
yk.password = 'redhat'

lc = User(username='liuChan', name='blue', email = 'blue@yahoo.com.cn')
lc.password = 'dsybs'

wq = User(username='wangqiang', name='wangQ', email='wq@qq.com')

db.session.add_all(yk,lc,wq)
db.session.commit()

statement = db.select([User]).where(
	or_( User.name == 'yangwawa0323', User.email.like('%qq.com'))
)
print(statement)

rows = db.session.execute(statement)
```



#### equals:

```
query.filter(User.name == 'leela')
```

#### not equals:

```
query.filter(User.name != 'leela')
```

#### LIKE:

```
query.filter(User.name.like('%leela%'))
```

#### IN:

```
query.filter(User.name.in_(['leela', 'akshay', 'santanu']))

# works with query objects too:

query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%santanu%'))))
```

#### NOT IN:

```
query.filter(~User.name.in_(['lee', 'sonal', 'akshay']))
```

#### IS NULL:

```
filter(User.name == None)
```

#### IS NOT NULL:

```
filter(User.name != None)
```

#### AND:

```
from sqlalchemy import and_
filter(and_(User.name == 'leela', User.fullname == 'leela dharan'))

#or, default without and_ method comma separated list of conditions are AND

filter(User.name == 'leela', User.fullname == 'leela dharan')

# or call filter()/filter_by() multiple times

filter(User.name == 'leela').filter(User.fullname == 'leela dharan')
```

#### OR:

```
from sqlalchemy import or_
filter(or_(User.name == 'leela', User.name == 'akshay'))
```

#### match:

```
query.filter(User.name.match('leela'))
```

### Flask 序列化

`jsonify`不能对数据模型的实例序列化，我们需要安装 **marshmallow** 来实现

```shell
pip install marshmallow
```

而在`models.py`建模中

```python
from marshmallow import Schema

class UserSchema(Schema):
    class Meta:
        fields = ('email', 'username', 'name')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #...
    name = db.Column(db.String(64))
```

而序列化的使用如下

```python
from app.models import User,UserSchema

users = User.query.all()

userSchema = UserSchema()
serialize = userSchema.dump(users,many=True)

print(serialize)
```

> 注意：在调用dump函数时，如果是多个对象（查询返回的list）需要添加 many=True, 否则无法正确序列化



## JWT 基于token令牌验证



### 基本用法

使用`create_access_token`函数形成一个新的访问**Token**, `jwt_required`装饰器用于保护 `endpoint`, `get_jwt_identity`函数用来获取受保护的 `endpoint`上的identity。

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run()
```

要访问受保护的`view`,需要在请求头中发送 **JWT** 信息，默认如下：

`Authentication: Bear <access_token>`

客户端先行提交账户密码信息验证，如果通过验证，将收到服务器给予的令牌

```shell
$ curl http://localhost:5000/protected
{
  "msg": "Missing Authorization Header"
}

$ curl http://localhost:5000/protected
{
  "msg": "Missing Authorization Header"
}

$ curl -H "Content-Type: application/json" -X POST \
  -d '{"username":"test","password":"test"}' http://localhost:5000/login
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwianRpIjoiZjhmNDlmMjUtNTQ4OS00NmRjLTkyOWUtZTU2Y2QxOGZhNzRlIiwidXNlcl9jbGFpbXMiOnt9LCJuYmYiOjE0NzQ0NzQ3OTEsImlhdCI6MTQ3NDQ3NDc5MSwiaWRlbnRpdHkiOiJ0ZXN0IiwiZXhwIjoxNDc0NDc1NjkxLCJ0eXBlIjoiYWNjZXNzIn0.vCy0Sec61i9prcGIRRCbG8e9NV6_wFH2ICFgUGCLKpc"
}

```

接着拿着**令牌**去访问受保护的 View

```shell
$ export ACCESS="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwianRpIjoiZjhmNDlmMjUtNTQ4OS00NmRjLTkyOWUtZTU2Y2QxOGZhNzRlIiwidXNlcl9jbGFpbXMiOnt9LCJuYmYiOjE0NzQ0NzQ3OTEsImlhdCI6MTQ3NDQ3NDc5MSwiaWRlbnRpdHkiOiJ0ZXN0IiwiZXhwIjoxNDc0NDc1NjkxLCJ0eXBlIjoiYWNjZXNzIn0.vCy0Sec61i9prcGIRRCbG8e9NV6_wFH2ICFgUGCLKpc"

$ curl -H "Authorization: Bearer $ACCESS" http://localhost:5000/protected
{
  "logged_in_as": "test"
}
```



### 部分保护

使用`jwt_optional`装饰器可以对 view 实现部分保护，作为可选项，如果可以获取到token信息，适用于A方案，否则B计划场景

```python
@app.route('/partial-protected', methods=('GET',))
@jwt_optional
def partial_protected():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_as_user=current_user), 200
    else:
        return jsonify(logged_as_user='Anonymous'), 200
```



### 用户自定义 token 中的附加信息

通过`@jwt.user_claims_loader`装饰器，指定一个函数，函数返回`JSON`格式信息将作为附加信息

```python
from flask_jwt_extended import get_jwt_claims
# Using the user_claims_loader, we can specify a method that will be
# called when creating access tokens, and add these claims to the said
# token. This method is passed the identity of who the token is being
# created for, and must return data that is json serializable
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'hello': identity,
        'foo': ['bar', 'baz']
    }

#...
# In a protected view, get the claims you added to the jwt with the
# get_jwt_claims() method
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    claims = get_jwt_claims()
    return jsonify({
        'hello_is': claims['hello'],
        'foo_is': claims['foo']
    }), 200
```



这样通过Chrome Advanced REST client 获取的请求将如下

![image-20200927174026789](./Flask%20%E5%85%A5%E9%97%A8.assets/image-20200927174026789.png)



## CoreUI

[Jinjia2 模版]()

```shell
git clone https://github.com/app-generator/theme-jinja2-coreui.git
```



##官方参考文档

* [Flask 1.1官方文档](https://flask.palletsprojects.com/en/1.1.x/)
* [flask-migrate数据库迁移库](https://flask-migrate.readthedocs.io/en/latest/)
* [flask-bootstrap前端框架](https://pythonhosted.org/Flask-Bootstrap/index.html)
* [bootstrap 3.4](https://getbootstrap.com/docs/3.4/css/)
* [SQLAlchemy数据库函数库](https://docs.sqlalchemy.org/en/13/)
* [Jinja2模版](https://jinja.palletsprojects.com/en/2.11.x/)
* [Vue 2.0前端框架](https://cn.vuejs.org/v2/guide/)
* [Jquery API前端框架](https://api.jquery.com/)
* [marshmallow序列化工具库](https://marshmallow.readthedocs.io/en/stable/quickstart.html)

