# Django Day05

## 反向解析

+ 用以不关注合法的URL如何修改，我们代码不做任何修改
+ 通过反向解析 urls.py 中的第三个参数 **name** 
  - 在模板中，我的用的是{% url %} 标签
  - 在views.py代码中，我们通过一个模块下的**reverse**函数

```python
from django.core.urlresolvers import reverse
def public_benefit(request):
    return redirect((reverse('public'))
```

### 正则表达式的分组名称

假设我们规划的时候想通过 /polls/detail/20/, /polls/detail/21/ 访问
+ 视图函数需要除了用户请求以外(第一个参数),还得有其他参数的传递
```python
def detail(request, question_id):
    ...
    pass
````

根据正则表达式 re 库,下面这段代码演示了分组操作

> (?P<名字>表达式) 一旦匹配后,我们将可以通过 QueryDict 雷同与Python的字典获取 key 对应的值

```python
import re
message = 'Yangkun got a mail send from joedoe@qq.com'
pattern = r'(?P<receiver>[A-Z][^ ]+).*\b(?P<sender>[a-z0-9]+@.*)'
m = re.match(pattern, message)
m.groupdict('receiver')
```

所以我们在 urls.py 中传参数给视图函数如下

```python
url(r'detail/(?P<question_text>[0-9]+)/$')
```

那就意味着 polls/detail/22 这个用户的请求将会变成
detail(HttpRequest object, question_id=22) 方式传给了我们的视图函数处理

## 表单搜索功能
1. 我们也应该规划一个网址.
2. 在母版中都能呈现出, {% url %} 方向解析
3. form 有**action**属性, 表单中的元素有**name**属性,才是一个合格的表单
4. 为了处理数据,还得有一套(网址的规划,视图函数,静态模板)

用户的搜索千奇百怪,可能直接在地址栏按照规律输入,比如 /polls/detail/10000000.
这样数据库中就搜索不到数据,但是Django视图会报错 **DoesNotExist**

## 显示公益页面的两种方法
定义一个视图函数渲染出公益页面
```python
def detail(request,qid):
    try:
        q = Question.objects.get(id=qid)
    except Question.DoesNotExist:
        return redirect(  reverse('public') )
        # return public_benefit(request)
    return render(request, 'polls/detail.html', { 'q': q} )


def public_benefit(request):
    return render(request, 'polls/public.html')
```
1. 直接呼叫其视图函数如上,  detail 函数出现 Question.DoesNotExist 异常以后,
直接呼叫 public_benefit 视图函数, public_benefit 会返回一个渲染的页面,我们同样返回即可
```python
return public_benefit(request)
```

2.以重定向的方式定位新的页面中,并且通过的是反向解析
```python
return redirect(  reverse('public') )
```
> redirect 函数实为快捷方式,from django.shortcuts import render,redirect
> 其实就是 django.http.HttpResponseRedirect 对象

