

# Oracle 11g 常用管理查询语句



# Linux 下环境变量设置

```shell
$ export ORACLE_HOME=/orahome/app/oracle/product/12.1.0.1/db_1
$ export ORACLE_SID=O12C
$ export LD_LIBRARY_PATH=/usr/lib:$ORACLE_HOME/lib
$ export PATH=$ORACLE_HOME/bin:$PATH  
```

默认Oracle数据搜索查询中区分字符的大小写，可以建立会话后设定两个变量

```plsql
---
ALTER SESSION SET NLS_COMP=LINGUISTIC;
ALTER SESSION SET NLS_SORT = BINARY_CI;
```



## 侦听实例状态

可以使用 `lsnrctl status` 查看实例启动状态

```shell
C:\Users\yangwawa>lsnrctl status

LSNRCTL for 64-bit Windows: Version 11.2.0.1.0 - Production on 02-SEP-2020 19:10:25

Copyright (c) 1991, 2010, Oracle.  All rights reserved.

Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC1521)))
STATUS of the LISTENER
------------------------
Alias                     LISTENER
Version                   TNSLSNR for 64-bit Windows: Version 11.2.0.1.0 - Production
Start Date                29-AUG-2020 23:23:57
Uptime                    3 days 19 hr. 46 min. 27 sec
Trace Level               off
Security                  ON: Local OS Authentication
SNMP                      OFF
Listener Parameter File   E:\app\yangwawa\product\11.2.0\dbhome_1\network\admin\listener.ora
Listener Log File         e:\app\yangwawa\diag\tnslsnr\DESKTOP-08E761I\listener\alert\log.xml
Listening Endpoints Summary...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(PIPENAME=\\.\pipe\EXTPROC1521ipc)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=127.0.0.1)(PORT=1521)))
Services Summary...
Service "orcl" has 1 instance(s).
  Instance "orcl", status READY, has 1 handler(s) for this service...
Service "orclXDB" has 1 instance(s).
  Instance "orcl", status READY, has 1 handler(s) for this service...
Service "rcat" has 1 instance(s).
  Instance "rcat", status READY, has 1 handler(s) for this service...
Service "rcatXDB" has 1 instance(s).
  Instance "rcat", status READY, has 1 handler(s) for this service...
The command completed successfully
```

* 也可以交互式查询

```shell
C:\Users\yangwawa>lsnrctl

LSNRCTL for 64-bit Windows: Version 11.2.0.1.0 - Production on 02-SEP-2020 19:11:35

Copyright (c) 1991, 2010, Oracle.  All rights reserved.

Welcome to LSNRCTL, type "help" for information.

LSNRCTL> services listener
Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC1521)))
Services Summary...
Service "orcl" has 1 instance(s).
  Instance "orcl", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:3344 refused:0 state:ready
         LOCAL SERVER
Service "orclXDB" has 1 instance(s).
  Instance "orcl", status READY, has 1 handler(s) for this service...
    Handler(s):
      "D000" established:0 refused:0 current:0 max:1022 state:ready
         DISPATCHER <machine: DESKTOP-08E761I, pid: 7112>
         (ADDRESS=(PROTOCOL=tcp)(HOST=DESKTOP-08E761I)(PORT=50731))
Service "rcat" has 1 instance(s).
  Instance "rcat", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:0 refused:0 state:ready
         LOCAL SERVER
Service "rcatXDB" has 1 instance(s).
  Instance "rcat", status READY, has 1 handler(s) for this service...
    Handler(s):
      "D000" established:0 refused:0 current:0 max:1022 state:ready
         DISPATCHER <machine: DESKTOP-08E761I, pid: 10752>
         (ADDRESS=(PROTOCOL=tcp)(HOST=DESKTOP-08E761I)(PORT=56243))
The command completed successfully
```

* 使用自带工具管理 **Oracle Net Manager** 

![image-20200902191509711](E:\Documents\Oracle11g常用管理查询.assets\image-20200902191509711.png)



* 建立数据库链接

  如果需要在不同的数据库之间查询数据，可以在当前实例中建立其他实例的数据库链接

  

![Description of create_database_link.gif follows](https://docs.oracle.com/cd/E11882_01/server.112/e41084/img/create_database_link.gif)



```plsql
 SQL>　CREATE DATABASE LINK orclInst
 2  　　CONNECT TO hr IDENTIFIED BY redhat USING 'orcl';
 SQL> DESC user_tables@orclInst;
```

> 建立链接之后在查询表后添加 `@linkname`  , 设置可以通过其他数据库的结构建表以及插入数据
>
> ```plsql
> CREATE TABLE orcl_user_tables AS SELECT * FROM user_tables@orclInst;
> INSERT INTO orcl_user_tables AS SELECT * FROM user_tables@orclInst;
> ```



## 逻辑结构和物理结构

![image-20200902203739335](E:\Documents\Oracle11g常用管理查询.assets\image-20200902203739335.png)

* 操作系统块: Windows/Linux 缺省为 4096, 4K
* Oracle 数据块： 2-32K ， 默认为8K，Windows/Linux 仅仅支持 2-16K， 参数 DB_BLOCK_SIZE
* 扩展段: 一系列Oracle数据块组成，在数据文件中一定是**连续**的
* 分段: 由一个或多个扩展段组成，也是连续的数字化

###　查看每个在数据库中的分段信息

```plsql
SQL>  select segment_type,count(1) from dba_segments group by segment_type
  2  order by segment_type;

SEGMENT_TYPE         COUNT(1)
------------------ ----------
CLUSTER                    10
INDEX                    3449
INDEX PARTITION           104
LOB PARTITION               1
LOBINDEX                  771
LOBSEGMENT                771
NESTED TABLE               26
ROLLBACK                    1
TABLE                    2210
TABLE PARTITION            88
TYPE2 UNDO                 10

11 rows selected.
```

![image-20200902210954533](E:\Documents\Oracle11g常用管理查询.assets\image-20200902210954533.png)



![image-20200902211630046](E:\Documents\Oracle11g常用管理查询.assets\image-20200902211630046.png)



```plsql
define tb=&tablespace;

select t.tablespace_name name, d.allocated, u.used, f.free,
t.status, d.cnt, contents, t.extent_management extman,
t.segment_space_management segman
from dba_tablespaces t,
(select sum(bytes) allocated, count(file_id) cnt from dba_data_files
where tablespace_name='&&tb') d,
(select sum(bytes) free from dba_free_space
where tablespace_name='&&tb') f,
(select sum(bytes) used from dba_segments
where tablespace_name='&&tb') u
where t.tablespace_name='&&tb';
```



![image-20200902213301719](E:\Documents\Oracle11g常用管理查询.assets\image-20200902213301719.png)



![image-20200902213314213](E:\Documents\Oracle11g常用管理查询.assets\image-20200902213314213.png)

![image-20200902213502168](E:\Documents\Oracle11g常用管理查询.assets\image-20200902213502168.png)



```plsql
CREATE SMALLFILE TABLESPACE "NEWTS"
DATAFILE 'D:\APP\ORACLE\ORADATA\ORCL11G\newts01.dbf'
SIZE 100M AUTOEXTEND ON NEXT 10M MAXSIZE 200M
LOGGING
EXTENT MANAGEMENT LOCAL
SEGMENT SPACE MANAGEMENT AUTO
DEFAULT NOCOMPRESS;
```



```plsql
SELECT t.name tablespace_name,
       d.name filename,
       d.bytes / 1024 / 1024 size_MB,
       d.create_bytes / 1024 / 1024 create_size_MB
FROM v$tablespace t JOIN v$tempfile d USING ( ts# )
WHERE t.name = 'TEMP';
```



# 管理控制文件

![image-20200831094804509](E:\Documents\Oracle11g常用管理查询.assets\image-20200831094804509.png)

* 显示控制文件存储信息

```plsql
SQL> select distinct type from v$controlfile_record_section;  
TYPE
----------------------------
FILENAME
TABLESPACE
RMAN CONFIGURATION
BACKUP CORRUPTION
PROXY COPY
FLASHBACK LOG
...
```

* 常看数据库相关信息

```plsql
SQL> select name, open_mode, created, current_scn from v$database;
NAME OPEN_MODE CREATED CURRENT_SCN
--------- -------------------- --------- -----------
O12C READ WRITE 27-SEP-14 319781
```

* 常看控制文件名字和位置

  + 方法一

    ```plsql
    SQL> show parameter control_files;
    ```

  + 方法二

    ```plsql
    SQL> select name from v$controlfile;
    ```

  + 方法三

    查看spfile中的字符串信息（仅仅适用于Linux）

    ```shell
    $ strings $ORACLE_HOME/dbs/spfileO12C.ora | grep -i control_files
    ```

    


## 在线重做日志

* 显示online redo log 信息

  从 `v$log` 和 `v$logfile` 动态视图表中查询

```pl
COL group# FORM 99999
COL thread# FORM 99999
COL grp_status FORM a10
COL member FORM a30
COL mem_status FORM a10
COL mbytes FORM 999999
--
SELECT
a.group#
,a.thread#
,a.status grp_status
,b.member member
,b.status mem_status
,a.bytes/1024/1024 mbytes
FROM v$log a,
v$logfile b
WHERE a.group# = b.group#
ORDER BY a.group#, b.member;

GROUP# THREAD# GRP_STATUS MEMBER MEM_STATUS MBYTES
------ ------- ---------- ------------------------------ ---------- -------
1 1 CURRENT /u01/oraredo/O12C/redo01a.rdo 50
1 1 CURRENT /u02/oraredo/O12C/redo01b.rdo 50
2 1 INACTIVE /u01/oraredo/O12C/redo02a.rdo 50
2 1 INACTIVE /u02/oraredo/O12C/redo02b.rdo 50
3 1 INACTIVE /u01/oraredo/O12C/redo03a.rdo 50
3 1 INACTIVE /u02/oraredo/O12C/redo03b.rdo 50
```

* 判断 Online redo log 分组大小

分析时间段

```plsql
select count(*)
,to_char(first_time,'YYYY:MM:DD:HH24')
from v$log_history
group by to_char(first_time,'YYYY:MM:DD:HH24')
order by 2;

COUNT(*) TO_CHAR(FIRST
---------- -------------
2 2014:09:24:04
80 2014:09:24:05
44 2014:09:24:06
10 2014:09:24:12
```

查看建议优化的日志文件大小

```plsql
SQL> select optimal_logfile_size from v$instance_recovery;
```



![image-20200831102429024](E:\Documents\Oracle11g常用管理查询.assets\image-20200831102429024.png)

* 添加日志分组

```plsql
alter database add logfile group 3
('/u01/oraredo/O12C/redo03a.rdo',
'/u02/oraredo/O12C/redo03b.rdo') SIZE 50M;
```

* 改变日志分组大小

```plsql
alter database add logfile group 4
('/u01/oraredo/O12C/redo04a.rdo',
'/u02/oraredo/O12C/redo04b.rdo') SIZE 200M;
```

```plsql
SQL> select group#, status, archived, thread#, sequence# from v$log;
```

* 删除分组

```plsql
SQL> alter database drop logfile group <group #>;
```

> [切换日志文件](#switch_logfile)
>
> 删除日志分组，并不会将系统的日志分组文件删除，需要手工删除。
>
> 删除日志分组，分组的状态必须为 **INACTIVE** ，如果删除当前在用的分组，`ORA-01623` 报错。
>
> - 切换日志文件
>
> ```plsql
> SQL> alter system switch logfile;
> ```
>
> - `ORA-01624` 报错，意味着日志分组需要做灾难恢复
>
> ```plsql
> SQL> alter system checkpoint;
> ```
>
> ```plsql
> SQL> select member from v$logfile;
> SQL> alter system switch logfile;
> SQL> /
> SQL> /
> ```

* 添加日志文件到分组中

```plsql
SQL> alter database add logfile member '/u02/oraredo/O12C/redo01b.rdo' to group 1;
```

* 移除分组中的日志文件

```plsql
SELECT a.group#, a.member, b.status, b.archived, SUM(b.bytes)/1024/1024 mbytes
FROM v$logfile a, v$log b
WHERE a.group# = b.group#
GROUP BY a.group#, a.member, b.status, b.archived
ORDER BY 1, 2;

SQL> alter database drop logfile member '/u01/oraredo/O12C/redo04a.rdo';
```

> 如果出现 `ORA-01623` 错误，需要切换日志，处理方式[如上](#switch_logfile)

* 移动日志文件或者改其名称

```plsql
SQL> shutdown immediate;

$ mv /u02/oraredo/O12C/redo02b.rdo /u01/oraredo/O12C/redo02b.rdo

SQL> startup mount;

SQL> alter database rename file '/u02/oraredo/O12C/redo02b.rdo'
to '/u01/oraredo/O12C/redo02b.rdo';

SQL> alter database open;
```



## 归档日志文件

* 设置归档日志位置

```plsql
SQL> alter system set log_archive_dest_1='location=/u01/oraarch/O12C' scope=both;
SQL> alter system set log_archive_format='O12C_%t_%s_%r.arc' scope=spfile;
```

> 在Linux下可以使用下面的命令检查
>
> ```shell
> $ cd $ORACLE_HOME/dbs
> $ strings spfile$ORACLE_SID.ora
> ```

>你可以通过 LOG_ARCHIVE_DESC_*N* 参数设置 
>
>```plsql
>SQL> show parameter log_archive_dest
>
>NAME TYPE VALUE
>---------------------- ----------- --------------------------
>log_archive_dest string
>log_archive_dest_1 string location=/u01/oraarch/O12C
>log_archive_dest_10 string
>```

* 查看详细的归档日志信息

```plsql
SQL> select dest_name, destination, status, binding from v$archive_dest;

DEST_NAME DESTINATION STATUS BINDING
-------------------- -------------------- --------- ---------
LOG_ARCHIVE_DEST_1 /u01/archive/O12C VALID OPTIONAL
LOG_ARCHIVE_DEST_2 INACTIVE OPTIONAL
...
```

## 日志文件 FRA 区域

开启FRA，设置以下两个参数

 ```plsql
SQL> alter system set db_recovery_file_dest_size=200g scope=both;

SQL> alter system set db_recovery_file_dest='/u01/fra' scope=both;

SQL> archive log list;

Database log mode Archive Mode
Automatic archival Enabled
Archive destination USE_DB_RECOVERY_FILE_DEST

SQL> show parameter db_recovery_file_dest

 ```

> 如果想同时设置FRA和非FRA位置
>
> ```plsql
> SQL> alter system set log_archive_dest_1='location=/u01/oraarch/O12C';
> SQL> alter system set log_archive_dest_2='location=USE_DB_RECOVERY_FILE_DEST';
> ```
>
> 关闭FRA
>
> ```plsql
> SQL> alter system set db_recovery_file_dest='';
> ```



## 归档日志

* 开启归档日志并检查

```plsql
SQL> shutdown immediate;
SQL> startup mount;
SQL> alter database archivelog;
SQL> alter database open;

SQL> archive log list;

SQL> select log_mode from v$database;
LOG_MODE
------------
ARCHIVELOG
```

* 关闭归档日志

```plsql
SQL> shutdown immediate;
SQL> startup mount;
SQL> alter database noarchivelog;
SQL> alter database open;
```

## 表空间和数据文件

![image-20200831151432277](E:\Documents\Oracle11g常用管理查询.assets\image-20200831151432277.png)

* 创建表空间

```plsql
create tablespace tools datafile '/u01/dbfile/O12C/tools01.dbf'
size 100m
segment space management auto;
--- OR
create tablespace tools datafile '/u01/dbfile/O12C/tools01.dbf'
size 100m
autoextend on maxsize 1000m
segment space management auto;
```

也可以使用变量的形式创建表空间

```plsql
define tbsp_large=5G
define tbsp_med=500M
--
create tablespace reg_data datafile '/u01/dbfile/O12C/reg_data01.dbf'
size &&tbsp_large segment space management auto;
--
create tablespace reg_index datafile '/u01/dbfile/O12C/reg_index01.dbf'
size &&tbsp_med segment space management auto;
```

> 上面的定义的变量在调用时使用 `&&` 

也可以写入到SQL脚本中

```plsql
define tbsp_large=&1
define tbsp_med=&2
--
create tablespace reg_data datafile '/u01/dbfile/O12C/reg_data01.dbf'
size &&tbsp_large segment space management auto;
--
create tablespace reg_index datafile '/u01/dbfile/O12C/reg_index01.dbf'
size &&tbsp_med segment space management auto;

SQL> @cretbsp 5G 500M
```

> 上面的 `&1` , `&2` 将作为位置参数
>
> 如果 `&varname` 将会提示你输入varname变量

* 查看已有的表空间是如何创建的

  使用 **DBMS_METADATA** 包中的函数

```plsql
SQL> set long 1000000

SQL> select dbms_metadata.get_ddl('TABLESPACE',tablespace_name) from dba_tablespaces;
```

* 修改表空间

```plsql
SQL> alter tablespace tools rename to tools_dev;
```

* 控制 redo 日志的生成

```plsql
create tablespace inv_mgmt_data
datafile '/u01/dbfile/O12C/inv_mgmt_data01.dbf' size 100m
segment space management auto
nologging;

SQL> select tablespace_name, logging from dba_tablespaces;
```

> 如果已有的表空间
>
> ```plsql
> SQL> alter tablespace inv_mgmt_data nologging;
> ```

* 改变表空间/表的读写模式

```plsql
SQL> alter tablespace inv_mgmt_rep read only;

SQL> alter tablespace inv_mgmt_rep read write;

SQL> alter table my_tab read only;

SQL> alter table my_tab read write;
```

* 删除表空间
  1. 先将表空间离线

```plsql
SQL> alter tablespace inv_data offline;
```

		2.  删除表空间包括内容和表空间中的数据文件

```plsql
SQL> drop tablespace inv_data including contents and datafiles;
```

> 如果遇到 ORA-02449: unique/primary keys in table referenced by foreign keys  错误
>
> ```plsql
> select p.owner,
> p.table_name,
> p.constraint_name,
> f.table_name referencing_table,
> f.constraint_name foreign_key_name,
> f.status fk_status
> from dba_constraints p,
> dba_constraints f,
> dba_tables t
> where p.constraint_name = f.r_constraint_name
> and f.constraint_type = 'R'
> and p.table_name = t.table_name
> and t.tablespace_name = UPPER('&tablespace_name')
> order by 1,2,3,4,5;
> ```
>
> 可以先行查询下 *inv_data* 表空间下存放表是否有外键参考的数据，查看表空间下表的约束
>
> 确定数据无关重要性后，可以使用 `CASCADE` 递归式删除
>
> ```plsql
> SQL> drop tablespace inv_data including contents and data files cascade constraints;
> ```



## RMAN 备份

* 查看备份集信息

```plsql
SET LINES 132 PAGESIZE 100
BREAK ON REPORT ON bs_key ON completion_time ON bp_name ON file_name
COL bs_key FORM 99999 HEAD "BS Key"
COL bp_name FORM a40 HEAD "BP Name"
COL file_name FORM a40 HEAD "Datafile"
--
SELECT
s.recid bs_key
,TRUNC(s.completion_time) completion_time
,p.handle bp_name
,f.name file_name
FROM v$backup_set s
,v$backup_piece p
,v$backup_datafile d
,v$datafile f
WHERE p.set_stamp = s.set_stamp
AND p.set_count = s.set_count
AND d.set_stamp = s.set_stamp
AND d.set_count = s.set_count
AND d.file# = f.file#
ORDER BY
s.recid
,p.handle
,f.name;
```

### 数据恢复

* 查看 **checkpoint**, 决定哪些数据需要恢复

```plsql
SET LINES 132
COL name FORM a40
COL status FORM A8
COL file# FORM 9999
COL control_file_SCN FORM 999999999999999
COL datafile_SCN FORM 999999999999999
--
SELECT
a.name
,a.status
,a.file#
,a.checkpoint_change# control_file_SCN
,b.checkpoint_change# datafile_SCN
,CASE
WHEN ((a.checkpoint_change# - b.checkpoint_change#) = 0) THEN 'Startup Normal'
WHEN ((b.checkpoint_change#) = 0) THEN 'File Missing?'
WHEN ((a.checkpoint_change# - b.checkpoint_change#) > 0) THEN 'Media Rec. Req.'
WHEN ((a.checkpoint_change# - b.checkpoint_change#) < 0) THEN 'Old Control File'
ELSE 'what the ?'
END datafile_status
FROM v$datafile a -- control file SCN for datafile
,v$datafile_header b -- datafile header SCN
WHERE a.file# = b.file#
ORDER BY a.file#;
```

* 查看数据文件头信息

```plsql
SQL> select file#, status, error, recover from v$datafile_header;
```

