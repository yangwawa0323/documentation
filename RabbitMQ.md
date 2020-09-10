

# Python RabbitMQ 消息队列



![logo](https://www.rabbitmq.com/img/logo-rabbitmq.svg)



## 使用容器方式运行

如果使用windows的用户，可以直接在容器中测试，避免复杂的安装 erlang 等环境，可以下载**docker desktop for windows**

```shell
docker pull rabbitmq:3

```

如果初次对RabbitMQ不熟悉，可以启动自带有管理WEB界面插件的容器

```shell
docker run -d --hostname my-rabbit --name some-rabbita -p 5672:5672 -p 8080:15672 rabbitmq:3-management
```

> 注意容器对宿主主机内存的反噬 `--memory 2048m` 或短格式 `-m 2048m`



## Python 开发库安装

```bash
python -m pip install pika --upgrade
```



### Producer和consumer 生产和消费模式

![img](https://www.rabbitmq.com/img/tutorials/python-one-overall.png)

#### Sending 发送

send.py

![img](https://www.rabbitmq.com/img/tutorials/sending.png)

```python
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
```



```python
channel.queue_declare(queue='hello')
```



```python
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
```



```python
connection.close()
```



### Receiving 接收

![img](https://www.rabbitmq.com/img/tutorials/receiving.png)

```python
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
```



```python
channel.queue_declare(queue='hello')
```



```python
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
```



```python
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)
```



```python
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```

```python
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
```



### 全部示例代码

**send.py**

```python
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
```

**receive.py**

```python
#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
```







![Hero](https://www.rabbitmq.com/img/home/banner/webinar/RabbitMQ-Hero-queues-desktop.svg)