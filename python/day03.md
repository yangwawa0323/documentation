# Python day03
## while 死循环
1. while True:
2. while 1 > 0:
由于在while判断条件永远的不变永久的成立，所以循环体永远执行
```python
while True:
    client, add_info = server_socket.accept()
    # 由于上面 accept的函数自身会阻塞,CPU不会被疯狂的消耗
```
> 死循环应该让处理至少喘一口气,一般会用time.sleep(0.05)

## while 当条件不满足后,退出循环
-----
## 文件的处理
### open()打开文件
1.第一个参数就是文件的路径
2.第二个参数为**模式**
| 字母 | 模式 | 特点 |
|---|---|---|
| r(默认模式)| readonly|只可以读取,**必须要提前存在,不可以写入**|
| w | writeonly | **不可读取,任何文件无论存在与否,直接成为零字节**(相当于bash "1>")
| a | append | 首先将文件文件定位 EOF, 相当于">>" |
| + |  | 弥补单个操作的不足
| w+ | | 以写为主,但也可以读取 |
| r+ | | 以读为主，但也可以写入 |
> w,a 模式都不可以读取

### 文件信息的处理操作
* .read() 一口气读取到 EOF,返回的一个整个字符串
> 但我们读取是个大数据的时候,比如3G大小的单个文件,我们应该设定一个大小的块,一个块一个快的读取,read(size)
* .readline() 一次一行
* .readline**s**() 将一行一行的数据读取到了一个列表中
> 不可以用在大数据的访问方式
* .write()
* .seek() 相当于磁带机倒带
  1.第一个参数就是跳转偏差值
  2.whence值(如下表)

| 值 | 方向 | 示意 |
| --- | ---| --- |
| 0 | --> | 从文件的起始处 |
| 1 | <-> | 从文件读到的当前位置(向前偏差值**负值**,向后用**正值**)|
| 2 | <-- | 从文件的 EOF 向前方向回退|

> python 操作文件,无论文件多大, 可以轻松的移动到开始处和结尾处(ms级)

* close() 文件
* with 的方法可以随手关闭文件
```python
import time

filename ='/tmp/testfile01.txt'

with open(filename) as fhandle:
    print fhandle.read()

time.sleep(100)
print "=" * 20
print "Bye Bye
```

## 异常
不正常的现象,出现异常以后,后续的代码立即终止,python执行代码的时候是变解释边执行的.
* NameError: 没有这种变量或函数名称
* IndexError: 超范围
* KeyError: 没有这个字典的key
* IOError: 文件的系统级访问出错
```python
try:
    a=10
    # print b
    alist = [ 1, 2 ,3 ]
    # print alist[10]
    adict = { 'name': 'ZSF'}

    # print adict['names']
    # f = open('/tmp/blablabla.txt')
    # print 1 / 0
except NameError:
    print "Variable is no defined"
except IndexError:
    print "Out of range"
except KeyError:
    print "Access wrong key"
except ZeroDivisionError:
    print "divsion must not be 0"
except IOError:
    print "File or directoty is no exists"

print "=" * 20
print "Bye bye"
```