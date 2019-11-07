# Django Day02

## PLAY WITH API

> 在已经建立好模的情况下,我们插入/查询CRUD?

```shell
python manage.py shell
```
已经加载了我们 django 运行环境变量

> 为了让我们有数据的生成可以实现CRUD
```python
import faker
from datetime import datetime
f = faker.Faker()

for i in range(300):
    qst = Question()
    qst.question_text = f.text()
    qst.pub_date = f.date_time_between_dates(  datetime.strptime('2019-1-1', '%Y-%m-%d'))
    qst.save()
```

+ 初始化一个Python对象,在内存中
+ .save() 将转换到数据库中
   - 如果是第一创建的对象,它**不具有 id 属性**,我们将用 **INSERT** 插入到数据库
   - 如果对原有的对象修改,它**已经具有 id 属性**, 将 **UPDATE** 到数据库

## 对象数据的查询
+ .objects.get() -> 单一的对象
   - 获取的必须是单一的一个,如果获取多个的时候,它保存
+ .objects.filter() -> 集合,list

### filter的语法
> 我们不能使用双下滑线去定义一切变量或者属性?
我们在过滤的时候,用到的公式 **变量__操作函数**

+ string_attr__*i*startswith 带*i* ignore_case,否则就使用 LIKE BINARY
+ string_attr__*i*endswith
+ int_attr__gt 大于
+ int_attr__gte greate or equal
+ int_attr__lt 小于
+ int_attr_lte 小与或等于

## 数据的删除
> .delete() 删除后是数据库中信息的消失，但是当前python对象还在，可以重新.save()。不过我们主键会自动增长。

## 时间之间的转换

+ datetime ---- datetime.strftime() ---> '2019-10-01'
+ '2019-10-1' ---- datetime.strptime() --->  datetime
+ longint ---- time.strftime()  ---> '2019-10-1'
+ datetime --- time.mktime( .timetuple()) ---> timetuple  ----> longint
+ longint ---> datetime.fromttimestamp() --> datetime

> time.mktime(datetime.timetuple(datetime.fromtimestamp( time.time())))
