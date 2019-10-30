# Python Day 02
---
> 注意: int / int 得到 int
float / int 得到 float
float(数值) / int
``` python
    + - * /
    % 取余数,求模
    // 取倍数
```
99 * 99 = 369729637649726772657187905628805440595668764281741102430259972423552570455277523421410650010128232727940978889548326540119429996769494359451621570193644014418071060667659301384999
779999159200499899**L**
L 长整型

## 歪八字运算
n = n + 1
n += 1 

## 数值
* 1.7e3 => 1700 => 1.7 * 10 * 10 * 10
* 1.7e-3 => 0.0017 => 1.7 / 10 / 10 / 10
* 0x80 十六进制 => 128

## 字符串
1. len() 字符串的长度
2. 第一个元素/字母都是从 **"0"** 开始的
3. 切片[起始:终止**之前**]
   * pystr[0:len(pytstr)]
   * pystr[0:100000]
   * pystr[:](标准)
4. 字符串 is immutable 不可以修改
   * _pystr[3] = 'a'_ 
   * TypeError: 'str' object does not support **item assignment**
5. 把字符串乘以多少数字,变成多少倍的输出
6. 把字符串的某个位置修改
   * 用字符串的衔接符号 "+", 去头去尾在加上别的字符
   * pystr[:6] 从零开始到第6+1个字符之前(默认开始处)
   * pystr[11:] 从11+1个字符开始到最后(默认到最后)
7. 反转的方式取字母
   * 最后一个就是 -1, -2 , -3
   * Hello
   * -5(H) ,-4(e), -3(l) , -2(l), -1(o)
8. 可以前方用正值,后面用负值

> 如何去除最后一个字母? 
如何去除第一个字母?

## List 列表 tuple 元组
> tuple只读

用**方括号**定义, 将来通过一头一尾的符号来识别定义的对象是什么
| 符号 |　对象的类型－意义 |
| --- | --- |
| " | 字符串 |
| [] | 列表 |
| () | tuple |
| {} | 字典 |

列表的最后一个元素后方可以跟随一个*逗号","*
列表的访问和字符串访问方式一致
1. len
2. [0] 元素的获取从**零**开始
3. 切片 [开始:结束之前]

> 列表是可以修改的 item assignment
4. people[-1] = 'Jakeson'
5. 取值/赋值的时候超出范围
IndexError: list assignment index **out of range**
6. tuple is immutable
   ```python
   officer = ( 'Zheng', 'Fu1', 'Fu2' )
   officer[-1] = 'Fu2' 
   #(错误的)
   ```

## 字典 dict
1. 不再按对应的位置,而是安装名字
2. index --> key
3. 字典一头一尾是一组**花括号"{}"**
4. { "key" : value, "key2": value , ...}
5. 字典优点:
   * 变长结构
   * 可以友好的名字来给要取的数据命名(key)
     example: host['port'], host['user'], host['protocol']
6. 查询不到key的时候
KeyError: 'password'
7. host['password'] = 'redhat' 给它赋值
   * 添加新的key
   * 修改已有key所对应的值
8. key就是属性,比如表述一个人的身高,年龄,姓名这些属性
   ```python
   person = {'height': 177, 'age':22, 'name':'Zhangsanfeng'}
   ```

## 代码块
缩进,python PEP8编程规范,默认**四个空格**
> Visual studio Code 有一个热键 **"Ctrl + Shift + I"**,也可以通过鼠标右击后弹出的菜单"Format Document"处理

## 条件判断
* if 条件成立:
___实施**A**计划
* if 条件成立:
___实施**A**计划
  else:
___Plan **B**
* if 符合条件1:
___Plan A
  elif 符合条件2:
___Plan B
  else:
___Plan C

## for 循环
```python
people = ['abc', 'yangkun','zhangsanfeng', 'zhaoliu']

for name in people:
    print name

```
1. for 变量名　in 集合／列表：　格式，变量名任意
2. 遍历，穷举，从头到尾全程经历一次

### for range 小孩子数数，数指头
1. range(8)　=> [0,1,2,3,4,5,6,7]
   * range(起始，终止**之前**) 默认起始就是０
   * range(0,10) == range(10) 
> 在python世界里面,有初学者最关键的函数
dir() 开宝箱看箱子里的宝贝
help() 看使用说明
2. 列表有一个**append()**方法

#### for 循环的进阶
```python
alist = [ 1, 4 ,8 , 21]
blist = [ ]
for a in alist:
    blist.append( a * 5 )
```
改良版
blist = [  a * 5   for a in alist     ]
1. 定义一个列表,然后撑撑成一个数组 blist = [                 ]
2. 在其中写个循环  blist = [    for  a in alist ]
3. 在循环前写要留下的变量 blist = [  a*5    for a in alist ]

```python
alist = range(3,18)
blist = [ ]
for a in alist:
    if a % 2 == 0:
        blist.append(a)
```
clist = [ a  for a in alist if a % 2 == 0 ]
改良版
1. 定义一个列表,然后撑撑成一个数组 blist = [                 ]
2. 在其中写个循环  blist = [    for  a in alist ]
3. 在循环后加入判断,中间不用添加冒号 blist = [  for a in alist  if a % 3 == 0
4. 在循环前写要留下的变量 blist = [  a   for a in alist if a % 3 == 0 ]

