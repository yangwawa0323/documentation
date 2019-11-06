# Python day04

## 函数
1. 代码段
2. 反复使用
3. 由繁化简
   

### 函数的格式
``` Python
   def foo():
       pass
```

``` python
　　def sayhello(lang):
       pass
```

### 常用模块
* faker 库
```python
  f = faker.Faker()
  f.email(), f.name(), f.female_name()
```
* random 库
```python
  random.choice( [ 'Male', 'Female' ]   )
```

### 函数中的缺省参数
```python
    def register(name, sex='F'):
        pass
    register('Elizabeth Bennett', 'F')
    # 使用缺省值 sex = 'F'
    register('Elizabeth Bennett')  
    # 替换默认sex值
    register('Elizabeth Bennett', 'M')
```
## 类,面向对象编程

1.具有方法的字典

2.构造器,也就是初始化方法,往往用来设置全新的对象 
```python
class Student:
    def __init__(self,name, age, sex):
        pass
```
3. self, 他/它/她自己