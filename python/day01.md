# Python 第一天

``` python
exam2 = "name: %s,  group: %d "
```

上面的例子中间,我们用到**格式化**字符串符号 "%"

| 符号    |  英文 | 意义     |
| --- | --- | --- |
| %s  | **S**tring | 此处填写的是字符串 |
| %d | **D**igit | 数值 |
| %f | **F**loat | 浮点 |
| %b | **B**oolean | 布尔值(True, False) |

## %f 的延伸

* %.2f   小数点后精度为两位(四舍五入)
* %10.2f 整体长度为10,(包括了小数点)
* %+10.2f 有正负值的符号

## %s 的延伸

* %-10s  左对齐
* %+10s  右对齐

## % 的使用

``` python
info = "Name: %s , Age: %+d, Weight: %+10.2f"

user = 'yangkun'
age = 43
weight =  65.5

print info % (user, age , weight)
```

    注意事项:
    1. 格式化符号的数量等同于输入的参数
    2. 对号入座

---

## raw_input

python 2.7 raw_input()
> *python 3.0 改成input()

> *raw_input 永远返回的是一个字符串,"45"
需要后期转型

## 转型的函数

| 原始类型 |　目标类型 | 函数　｜
| --- | --- | --- |
| s | i | int() |
| s | f | float() |
| s | b | bool() |
| 任何 | s | str() |

> type() 用来识别数据类型

> pass 代表什么也不做,满足语言缩进等格式

## 导入别人的成果,导入函数库

import xxxx 相当于借了一个**工具箱**

> xxxx.py (省掉.py后缀)

dir(xxxx) 查看工具箱的**工具**

> **xxxx**.*yyyy* 某某工具箱下的某个工具

help(xxxx.yyyy) 查看工具箱中的工具的使用说明

> SyntaxError: Non-ASCII character '\xe8' in file mylib.py on line 4, but no encoding declar
ed; see [detail](link=http://python.org/dev/peps/pep-0263/) for details, 代表着多半是因为程序中有中文,**中文空格**, 在程序头部 **coding: utf-8**

> 在一个定义函数下,紧接着写的字符串,将会成为这个函数的说明文档

## 引号的使用

* 单个的引号,纯字符串,不可以跨行,当要换行的时候,用承上接下符号"\"
* 三个个引号,可以跨行,可以包括单个引号的应用
