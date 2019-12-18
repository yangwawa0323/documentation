# Django REST 框架

## 1. 建立模型

> 与平时建立Django模型无异

```python
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']
```

## 2.创建Serializers类

宣称一个如同Django中的forms一样的serializers类. 此时需要在 app 下创建一个 serializers.py 程序

```python
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
```



## 2.2 使用 ModelSerializers

与Form类和ModelForm一样, REST 框架也包括了Serializer类和ModelSerializer类.

```python
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
```

一旦属性字段定义之后,你可以查看serializer实例中所有的字段,并可以打印出来

```python
from snippets.serializers import SnippetSerializer
serializer = SnippetSerializer()
print(repr(serializer))
# SnippetSerializer():
#    id = IntegerField(label='ID', read_only=True)
#    title = CharField(allow_blank=True, max_length=100, required=False)
#    code = CharField(style={'base_template': 'textarea.html'})
#    linenos = BooleanField(required=False)
#    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'), ('abap', 'ABAP'), ('ada', 'Ada')...
#    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')...
```





## 2.3 命令行下serializers测试

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print("hello, world")\n')
snippet.save()

serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}

content = JSONRenderer().render(serializer.data)
content
# b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'

import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)

serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()

# <Snippet: Snippet object>
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
# [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```



## 3. 在 views.py 中使用我们定义的serializers

> 注意,为了防止跨越站点的主机向我们提交CSFS的POST请求,我们对每个 view 使用了 csrf_exempt 装饰器

```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
    
```



## 4.最后我们定义 urls.py

```python
from django.conf.urls import url
from . import views

urlpatterns = [
    url('snippets/', views.snippet_list),
    url('snippets/<int:pk>/', views.snippet_detail),
]
```



## 附录学习笔记

* 在使用 RESTFUL 方式编程的时候, 提供给小程序 serializer 的代码(也就是 JSON 格式) 都放在 **{project}/{app}/ api/** 目录下, 这样{project}/{app}/的代码作用给 WEB, 而{project}/{app}/api 作用给小程序,将两者很好的区分开.

  > 注: rest framework 中有很多的机制值得借鉴，比如阈值的设置，防止爬虫或者恶意刷新请求

* serializers.**ModelSerializer**

  * class **Meta**:

    * model 属性定义模型

    * fields 属性定义了返回的 JSON 格式中包括此模型中的哪些字段

    * extra_kwargs 定义额外的属性

      * ```python
        extra_kwargs = { 'password': { 'write_only': True}}
        ```
  
  
  
* viewsets.**ModelViewSet**

  * authentication_classes

  * serializer_class

  * queryset

    

* CreateAPIView 中的方法

  * perform_create(self,serializer) 可以实现对象创建时的自定义行为

    ```python
    class PostCreateAPIView(CreateAPIView):
        queryset = Post.objects.all()
        serializer_class = PostCreateUpdateSerializer
        
        def perform_create(self, serializer):
            serializer.save(user=self.request.user)
    ```

    以上代码在提交一个新的 Post 对象的时候,从用户请求中获取user对象,设置给 Post中user属性(其为一个指向**Django.contrib.auth.models.User**的ForeignKey字段) 

    

* rest_frameworks.routers.**DefaultRouter**
  * ```python
    router = DefaultRouter()
    router.register('sub_path_of_url', views.ViewSet, base_name='reverse_name')
    ```
  
  
  
* throttle 控制, 限制访问的频率
  
  * **UserRateThrottle** 用户访问频率控制
    
  * ```python
    from rest_framework.decorators import api_view, throttle_classes
    from rest_framework.throttling import UserRateThrottle
    class OncePerDayUserThrottle(UserRateThrottle):
        rate = '1/day'
        
    @api_view(['GET'])
    @throttle_classes([OncePerDayUserThrottle])
    def view(request):
      return Response({"message": "Hello for today! See you tomorrow!"})
    ```
    
  * 每个阈值的控制都是基于每个请求的IP地址生成 Unique Key 来统计计算的
  
  - 
  
* 以下装饰器都需要跟随 @api_view 使用,参数都为列表

  - @renderer_classes(...)
  - @parser_classes(...)
  - @authentication_classes(...)
  - @throttle_classes(...)
  - @permission_classes(...)

* SimpleRouter 提供了一系列标准路由

  * list

  * create

  * retrieve

  * update

  * partitial_update

  * destroy

    | URL 样式  | HTTP 方法 | 动作 | URL名称 |
    | --------- | --------- | ---- | ------- |
    | {prefix}/ | GET       |  list   |  {basename}-list       |
    | {prefix}/ | POST      | create  | {basename}-list |
| {prefix}/{url_path} | GET 或者指定的 methods 的参数 | `@action(detail=False)` 装饰器方法 | {basename}-{url_name} |
    | {prefix}/{lookup}/ | GET | retrieve | {basename}-detail |
    | {prefix}/{lookup}/ | PUT | update | {basename}-detail |
    | {prefix}/{lookup}/ | PATCH | partial_update | {basename}-detail |
    | {prefix}/{lookup}/ | DELETE | destroy | {basename}-detail |
    
    