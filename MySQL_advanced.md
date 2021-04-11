# MySQL 集群高阶篇

企业高可用性标准,全年无故障率(非计划内故障停机)

```rust
99.9%                 ----> 0.001*365*24*60=525.6  min
99.99%                ----> 0.0001*365*24*60=52.56 min
99.999%               ----> 0.0001*365*24*60=5.256 min
```



## 高可用架构方案

* 负载均衡:有一定的高可用性 
LVS  Nginx
* 主备系统:有高可用性,但是需要切换,是单活的架构
KA ,   MHA,  MMM
* 真正高可用(多活系统): 
NDB Cluster  Oracle RAC  Sysbase cluster   , InnoDB Cluster（MGR）,PXC , MGC


###  主从复制简介    

1.1. 基于二进制日志复制的
1.2. 主库的修改操作会记录二进制日志
1.3. 从库会请求新的二进制日志并回放,最终达到主从数据同步
1.4. 主从复制核心功能:
辅助备份,处理物理损坏                   
扩展新型的架构:高可用,高性能,分布式架构等


### 2. 主从复制前提(搭建主从的过程)     




2.1 两台以上mysql实例 ,server_id,server_uuid不同
2.2 主库开启二进制日志
2.3 专用的复制用户
2.4 保证主从开启之前的某个时间点,从库数据是和主库一致(补课)
2.5 告知从库,复制user,passwd,IP port,以及复制起点(change master to)
2.6 线程(三个):Dump thread  IO thread  SQL thread 开启(start slave)


###  主从复制搭建(Classic replication)   


####  清理主库数据

```shell
$ rm -rf /data/3307/data/*
```

#### 重新初始化3307

```shell
mysqld --initialize-insecure --user=mysql --basedir=/app/mysql --datadir=/data/3307/data
```

####  修改my.cnf ,开启二进制日志功能

```shell
$ vim /data/3307/my.cnf 
log_bin=/data/3307/data/mysql-bin
```

#### 启动所有节点

```shell
# systemctl start mysqld3307
# systemctl start mysqld3308
# systemctl start mysqld3309
# ps -ef |grep mysqld
mysql      3684      1  4 09:59 ?        00:00:00 /app/mysql/bin/mysqld --defaults-file=/data/3307/my.cnf
mysql      3719      1  7 09:59 ?        00:00:00 /app/mysql/bin/mysqld --defaults-file=/data/3308/my.cnf
mysql      3754      1  8 09:59 ?        00:00:00 /app/mysql/bin/mysqld --defaults-file=/data/3309/my.cnf
# mysql -S /data/3307/mysql.sock -e "select @@server_id"
# mysql -S /data/3308/mysql.sock -e "select @@server_id"
# mysql -S /data/3309/mysql.sock -e "select @@server_id"
```

#### 主库中创建复制用户

```shell
# mysql -S /data/3307/mysql.sock 
db01 [(none)]> grant replication slave on *.* to repl@'10.0.0.%' identified by '123';
db01 [(none)]> select user,host from mysql.user;
```



#### 备份主库并恢复到从库

```shell
# mysqldump -S /data/3307/mysql.sock -A --master-data=2 --single-transaction  -R --triggers >/backup/full.sql
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=653;
# mysql -S /data/3308/mysql.sock
db01 [(none)]> source /backup/full.sql
```



####  告知从库关键复制信息

```shell
ip port user  password  binlog position 
[root@db01 3307]# mysql -S /data/3308/mysql.sock
mysql> help change master to

CHANGE MASTER TO
  MASTER_HOST='10.0.0.51',
  MASTER_USER='repl',
  MASTER_PASSWORD='123',
  MASTER_PORT=3307,
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=653,
  MASTER_CONNECT_RETRY=10;
```

#### 开启主从专用线程

```mysql
start slave ;
```

#### 检查复制状态

```mysql
db01 [mysql]>show slave  status \G
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```

###  主从复制的原理 (Classic Replication)

#### 主从中设置到的文件和线程

##### 线程

主:
DUMP THREAD
从:
IO  THREAD
SQL THREAD


##### 文件

主:
mysql-bin.000001
从: 
db01-relay.000001     ===>中继日志
master.info                 ===》主库信息记录日志
relay-log.info              ===> 记录中继应用情况信息


####   主从复制原理

![img](https:////upload-images.jianshu.io/upload_images/16956686-72dd1f45d206d507.png?imageMogr2/auto-orient/strip|imageView2/2/w/693/format/webp)



![img](https:////upload-images.jianshu.io/upload_images/16956686-a4273ecc8aa1c370.png?imageMogr2/auto-orient/strip|imageView2/2/w/724/format/webp)



主从复制原理描述：

1. **change master to** 时，`ip pot user password binlog position`写入到`master.info`进行记录

2. **start slave** 时，从库会启动IO线程和SQL线程
3. IO_T，读取master.info信息，获取主库信息连接主库
4. 主库会生成一个准备`binlog `DUMP线程，来响应从库
5. IO_T根据master.info记录的binlog文件名和position号，请求主库DUMP最新日志
6. DUMP线程检查主库的binlog日志，如果有新的，TP(传送)给从从库的IO_T
7. IO_T将收到的日志存储到了TCP/IP 缓存，立即返回ACK给主库 ，主库工作完成
    8.IO_T将缓存中的数据，存储到relay-log日志文件,更新master.info文件binlog 文件名和postion，IO_T工作完成
    9.SQL_T读取relay-log.info文件，获取到上次执行到的relay-log的位置，作为起点，回放relay-log
    10.SQL_T回放完成之后，会更新relay-log.info文件。
8. relay-log会有自动清理的功能。
   细节：
   1.主库一旦有新的日志生成，会发送“信号”给binlog dump ，IO线程再请求


### 主从故障监控\分析\处理 

#### 线程相关监控

##### 主库:

```mysql
show full processlist;
每个从库都会有一行dump相关的信息
HOSTS: 
db01:47176
State:
Master has sent all binlog to slave; waiting for more updates
如果现实非以上信息,说明主从之间的关系出现了问题    
```

#####  从库:

```mysql
db01 [(none)]>show slave status \G
*************************** 1. row ***************************
```

####  主库相关信息监控

```mysql
Master_Host: 10.0.0.51
Master_User: repl
Master_Port: 3307
Master_Log_File: mysql-bin.000005
Read_Master_Log_Pos: 444
```

#### 从库中继日志的应用状态

```mysql
Relay_Log_File: db01-relay-bin.000002
Relay_Log_Pos: 485
```

#### 从库复制线程有关的状态

```mtsql
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
Last_IO_Errno: 0
Last_IO_Error: 
Last_SQL_Errno: 0
Last_SQL_Error: 
```

#### 过滤复制有关的状态

Replicate_Do_DB: 
Replicate_Ignore_DB: 
Replicate_Do_Table: 
Replicate_Ignore_Table: 
Replicate_Wild_Do_Table: 
Replicate_Wild_Ignore_Table: 


#### 主从延时相关状态(非人为)

**Seconds_Behind_Master**: 0


#### 延时从库有关的状态(人为)

SQL_Delay: 0
SQL_Remaining_Delay: NULL


#### GTID 复制有关的状态

Retrieved_Gtid_Set: 
Executed_Gtid_Set: 
Auto_Position: 0


####  主从复制故障分析

##### 连接主库

(1) 用户 密码  IP  port

```shell
Last_IO_Error: error reconnecting to master 'repl@10.0.0.51:3307' - retry-time: 10  retries: 7
# mysql -urepl  -p123333  -h 10.0.0.51 -P 3307
ERROR 1045 (28000): Access denied for user 'repl'@'db01' (using password: YES)
```

原因:
密码错误 
用户错误 
skip_name_resolve
地址错误
端口


![img](https:////upload-images.jianshu.io/upload_images/16956686-2d45278fb16e4d69.png?imageMogr2/auto-orient/strip|imageView2/2/w/932/format/webp)


![img](https:////upload-images.jianshu.io/upload_images/16956686-0ed17c75c871d787.png?imageMogr2/auto-orient/strip|imageView2/2/w/975/format/webp)



##### 处理方法

```mysql
mysql> stop  slave  
mysql> reset slave all 
mysql> change master to 
mysql> start slave
```



##### 主库连接数上线,或者是主库太繁忙

```mysql
show slave  staus \G 
Last_IO_Errno: 1040
Last_IO_Error: error reconnecting to master 'repl@10.0.0.51:3307' - retry-time: 10  retries: 7
处理思路:
拿复制用户,手工连接一下

[root@db01 ~]# mysql -urepl -p123 -h 10.0.0.51 -P 3307 
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1040 (HY000): Too many connections
处理方法:
db01 [(none)]>set global max_connections=300;

(3) 防火墙,网络不通
```



#### 请求二进制日志

主库缺失日志
从库方面,二进制日志位置点不对
`Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'could not find next log; the first event 'mysql-bin.000001' at 154, the last event read from '/data/3307/data/mysql-bin.000002' at 154, the last byte read from '/data/3307/data/mysql-bin.000002' at 154.'`


![img](https:////upload-images.jianshu.io/upload_images/16956686-78c7eaaacd175fc0.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)


> 注意: 在主从复制环境中,严令禁止主库中reset master; 可以选择expire 进行定期清理主库二进制日志
解决方案:
重新构建主从




####  SQL 线程故障

##### SQL线程功能：

1. 读写`relay-log.info` 
2. `relay-log`损坏,断节,找不到
3. 接收到的SQL无法执行



##### 导致SQL线程故障原因分析：


1. 版本差异，参数设定不同，比如：数据类型的差异，`SQL_MODE`影响

2. 要创建的数据库对象,已经存在

3. 要删除或修改的对象不存在  

4. DML语句不符合表定义及约束时.  

  归根揭底的原因都是由于从库发生了写入操作.
  `Last_SQL_Error: Error 'Can't create database 'db'; database exists' on query. Default database: 'db'. Query: 'create database db'`



##### 处理方法(以从库为核心的处理方案)：

方法一：

```mysql
mysql> stop slave; 
mysql> set global sql_slave_skip_counter = 1;
```

> 将同步指针向下移动一个，如果多次不同步，可以重复操作。

```mysql
mysql> start slave;
```

 方法二：
 /etc/my.cnf
 **slave-skip-errors** = 1032,1062,1007
 常见错误代码:
 `1007`:对象已存在
 `1032`:无法执行DML
 `1062`:主键冲突,或约束冲突

但是，以上操作有时是有风险的，最安全的做法就是重新构建主从。把握一个原则,一切以主库为主.



##### 一劳永逸的方法:

1. 可以设置从库只读.

```mysql
mysql> show variables like '%read_only%';
```

> 注意：
> 只会影响到普通用户，对管理员用户无效。

2. 加中间件
   读写分离。



#### 主从延时监控及原因

主库做了修改操作,从库比较长时间才能追上.

#####  外在因素

网络 
主从硬件差异较大
版本差异
参数因素

##### 主库

1. 二进制日志写入不及时

```mysql
select @@sync_binlog;
```



2. `CR`的主从复制中,`binlog_dump`线程,事件为单元,串行传送二进制日志(5.6 5.5)
   1. 主库并发事务量大,主库可以并行,传送时是串行
   2. 主库发生了大事务,由于是串行传送,会产生阻塞后续的事务.

解决方案:
1. `5.6 `开始,开启**GTID**,实现了`GC`(group commit)机制,可以并行传输日志给从库IO
2. `5.7 `开始,不开启**GTID**,会自动维护匿名的`GTID`,也能实现`GC`,我们建议还是认为开启`GTID`
3. 大事务拆成多个小事务,可以有效的减少主从延时.

#### 从库

`SQL`线程导致的主从延时
在`CR`复制情况下: 从库默认情况下只有一个SQL,只能串行回放事务SQL

1. 主库如果并发事务量较大,从库只能串行回放
2. 主库发生了大事务,会阻塞后续的所有的事务的运行

解决方案:
1. 5.6 版本开启`GTID`之后,加入了SQL多线程的特性,但是只能针对不同库(database)下的事务进行并发回放.
2. 5.7 版本开始`GTID`之后,在SQL方面,提供了基于逻辑时钟(logical_clock),**binlog**加入了`seq_no`机制,
真正实现了基于事务级别的并发回放,这种技术我们把它称之为**MTS**(`enhanced multi-threaded slave`).
3. 大事务拆成多个小事务,可以有效的减少主从延时.
[https://dev.mysql.com/worklog/task/?id=6314]



------

## MySQL Group Replication 介绍

基于传统异步复制和半同步复制的缺陷——数据的一致性问题无法保证，MySQL官方在5.7.17版本正式推出组复制（MySQL Group Replication，简称MGR）。

由若干个节点共同组成一个复制组，一个事务的提交，必须经过组内大多数节点（N / 2 + 1）决议并通过，才能得以提交。如上图所示，由3个节点组成一个复制组，Consensus层为一致性协议层，在事务提交过程中，发生组间通讯，由2个节点决议(certify)通过这个事务，事务才能够最终得以提交并响应。

引入组复制，主要是为了解决传统异步复制和半同步复制可能产生数据不一致的问题。组复制依靠分布式一致性协议(Paxos协议的变体)，实现了分布式下数据的最终一致性，提供了真正的数据高可用方案(是否真正高可用还有待商榷)。其提供的多写方案，给我们实现多活方案带来了希望。

![img](https:////upload-images.jianshu.io/upload_images/16956686-b6b4088d046b6cf4.png?imageMogr2/auto-orient/strip|imageView2/2/w/931/format/webp)



###  创建用户

```shell
$ useradd mysql
```



### 上传5.7.20软件到/usr/local解压

```shell
$ tar -zxvf mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz 
$ mv mysql-5.7.20-linux-glibc2.12-x86_64/  mysql
```



### 环境变量



```shell
$ vi /root/.bash_profile
export PATH=$PATH:/usr/local/mysql/bin

$ mkdir -p /data/3306/data  /data/3307/data /data/3308/data
$ chown -R mysql.mysql /data /usr/local/mysql
```



### 配置文件说明

配置示例：
++++++++++3306++++++
[mysqld]
user=mysql
datadir=/data/3306/data
basedir=/usr/local/mysql
port=3306
socket=/data/3306/mysql.sock
server_id=1
gtid_mode=ON
enforce_gtid_consistency=ON
master_info_repository=TABLE
relay_log_info_repository=TABLE
binlog_checksum=NONE
log_slave_updates=ON
log_bin=binlog
binlog_format=ROW
transaction_write_set_extraction=XXHASH64
loose-group_replication_group_name="22d56f7c-dfe5-4eb1-a21a-cf9c27e8d625"
loose-group_replication_start_on_boot=off
loose-group_replication_local_address="192.168.29.128:33061"
loose-group_replication_group_seeds="192.168.29.128:33061,192.168.29.128:33062,192.168.29.128:33063"
loose-group_replication_bootstrap_group=off
loose-group_replication_single_primary_mode=FALSE
loose-group_replication_enforce_update_everywhere_checks= TRUE

++++++++++3307++++++
[mysqld]
user=mysql
datadir=/data/3307/data
basedir=/usr/local/mysql
port=3307
socket=/data/3307/mysql.sock
server_id=2
gtid_mode=ON
enforce_gtid_consistency=ON
master_info_repository=TABLE
relay_log_info_repository=TABLE
binlog_checksum=NONE
log_slave_updates=ON
log_bin=binlog
binlog_format=ROW
transaction_write_set_extraction=XXHASH64
loose-group_replication_group_name="22d56f7c-dfe5-4eb1-a21a-cf9c27e8d625"
loose-group_replication_start_on_boot=off
loose-group_replication_local_address="192.168.29.128:33062"
loose-group_replication_group_seeds="192.168.29.128:33061,192.168.29.128:33062,192.168.29.128:33063"
loose-group_replication_bootstrap_group=off
loose-group_replication_single_primary_mode=FALSE
loose-group_replication_enforce_update_everywhere_checks= TRUE

++++++++++3308++++++
[mysqld]
user=mysql
datadir=/data/3308/data
basedir=/usr/local/mysql
port=3308
socket=/data/3308/mysql.sock
server_id=3
gtid_mode=ON
enforce_gtid_consistency=ON
master_info_repository=TABLE
relay_log_info_repository=TABLE
binlog_checksum=NONE
log_slave_updates=ON
log_bin=binlog
binlog_format=ROW
transaction_write_set_extraction=XXHASH64
loose-group_replication_group_name="22d56f7c-dfe5-4eb1-a21a-cf9c27e8d625"
loose-group_replication_start_on_boot=off
loose-group_replication_local_address="192.168.29.128:33063"
loose-group_replication_group_seeds="192.168.29.128:33061,192.168.29.128:33062,192.168.29.128:33063"
loose-group_replication_bootstrap_group=off
loose-group_replication_single_primary_mode=FALSE
loose-group_replication_enforce_update_everywhere_checks= TRUE

组复制部分，配置文件介绍：
group_replication变量使用的loose-前缀是指示Server启用时尚未加载复制插件也将继续启动

**transaction_write_set_extraction** = XXHASH64

> 指示Server必须为每个事务收集写集合，并使用XXHASH64哈希算法将其编码为散列

**loose-group_replication_group_name**="01e5fb97-be64-41f7-bafd-3afc7a6ab555"

> 表示将加入或者创建的复制组命名为01e5fb97-be64-41f7-bafd-3afc7a6ab555
> 可自定义(通过cat /proc/sys/kernel/random/uuid)

**loose-group_replication_start_on_boot**=off 

> 设置为Server启动时不自动启动组复制

**loose-group_replication_local_address**="192.168.29.128:33061" 

> 绑定本地的192.168.29.128及33061端口接受其他组成员的连接，IP地址必须为其他组成员可正常访问

**loose-group_replication_group_seeds**="192.168.29.128:33061,192.168.29.128:33062,192.168.29.128:33063"

> 本行为告诉服务器当服务器加入组时，应当连接到192.168.29.128:33061,192.168.29.128:33062,192.168.29.128:33063
> 这些种子服务器进行配置。本设置可以不是全部的组成员服务地址。

**loose-group_replication_bootstrap_group** = off 
> 配置是否自动引导组

**loose-group_replication_ip_whitelist**=”10.30.0.0/16,10.31.0..0/16,10.27.0.0/16″
> 配置白名单，默认情况下只允许192.168.29.128连接到复制组，如果是其他IP则需要配置。



### 初始化数据,并启动数据库节点

首先数据库的启动需要对应的系统表和表空间等文件，我们要对三个实例的目录进行初始化

```shell
/usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/3306/data

/usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/3307/data

/usr/local/mysql/bin/mysqld --initialize-insecure  --user=mysql --basedir=/usr/local/mysql --datadir=/data/3308/data

mysqld_safe --defaults-file=/data/3306/my.cnf &
mysqld_safe --defaults-file=/data/3307/my.cnf &
mysqld_safe --defaults-file=/data/3308/my.cnf &
```

> **--initialize-insecure** 初始化，MySQL实例的密码为空，也可以通过 **--initialize** 初始化，MySQL将为你生成一个复杂的密码，可以通过 log-error 日志查看



#### 3306节点加入GR

创建复制用户
```mysql
shell$ mysql -S /data/3306/mysql.sock
mysql> set sql_log_bin=0;
mysql> grant replication slave,replication client on *.* to repl@'localhost' identified by '123';
mysql> grant replication slave,replication client on *.* to repl@'127.0.0.1' identified by '123';
mysql> grant replication slave,replication client on *.* to repl@'192.168.29.%' identified by '123';
mysql> SET SQL_LOG_BIN=1;
mysql> change master to master_user='repl',master_password='123' for channel 'group_replication_recovery';
```

> 注：如果为三台独立节点，需要将localhost、127.0.0.1和远程主机域都授权用户
开启分布式复制
> set sql_log_bin = 0 ; 非常关键，它临时的禁用了语句添加到binlog中，因为我们在其他主机上也要手工创建GR的账户，如果日志中记录了create user的语句，这样在分组复制的过程中此事务处理通不过，会造成复制停滞的反复重试，严重时会导致复制失败。


加载GR插件

```mysql
install plugin group_replication soname 'group_replication.so';
show plugins;
```

启动复制程序
```mysql
set global group_replication_bootstrap_group=ON;
start group_replication;
set global group_replication_bootstrap_group=OFF;
```
> 之所以将 `group_replication_bootstrap_group` 不添加到配置文件中，是因为只要在确认为初始化的主服务器上开启一次，而其他组成员不需要启用。所以采用手工的方式。

检测组是否创建并已加入新成员
```mysql
select * from performance_schema.replication_group_members;
```

#### 3307加入GR：



```mysql
创建复制用户
mysql -S /data/3307/mysql.sock
set sql_log_bin=0;
 grant replication slave,replication client on *.* to repl@'localhost' identified by '123';
 grant replication slave,replication client on *.* to repl@'127.0.0.1' identified by '123';
 grant replication slave,replication client on *.* to repl@'192.168.29.%' identified by '123';
 SET SQL_LOG_BIN=1;
 注：如果为三台独立节点，需要将localhost、127.0.0.1和远程主机域都授权用户
 开启分布式复制
 change master to master_user='repl',master_password='123' for channel 'group_replication_recovery';

加载GR插件
install plugin group_replication soname 'group_replication.so';
show plugins;

启动复制程序
start group_replication;

#检测组是否创建并已加入新成员
select * from performance_schema.replication_group_members;

注： 前面的用户密码修改和创建用户操作必须设置binlog不记录，执行后再打开，否则会引起START GROUP_REPLICATION执行报错:
ERROR 3092 (HY000): The server is not configured properly to be an active member of the group. Please see more details on error log.
解决方案是：根据提示打开group_replication_allow_local_disjoint_gtids_join选项，mysql命令行执行:
mysql> set global group_replication_allow_local_disjoint_gtids_join=ON;
然后再执行:
mysql> start group_replication;
```



#### 3308加入GR



```mysql
创建复制用户
mysql -S /data/3308/mysql.sock
set sql_log_bin=0;
 grant replication slave,replication client on *.* to repl@'localhost' identified by '123';
 grant replication slave,replication client on *.* to repl@'127.0.0.1' identified by '123';
 grant replication slave,replication client on *.* to repl@'192.168.29.%' identified by '123';
 set sql_log_bin=1;

 注：如果为三台独立节点，需要将localhost、127.0.0.1和远程主机域都授权用户

 开启分布式复制
 change master to master_user='repl',master_password='123' for channel 'group_replication_recovery';

加载GR插件
install plugin group_replication soname 'group_replication.so';
show plugins;

启动复制程序
start group_replication;
#检测组是否创建并已加入新成员
select * from performance_schema.replication_group_members;
```



