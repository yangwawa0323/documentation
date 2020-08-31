# Oracle 11g 常用管理查询语句



# Linux 下环境变量设置

```shell
$ export ORACLE_HOME=/orahome/app/oracle/product/12.1.0.1/db_1
$ export ORACLE_SID=O12C
$ export LD_LIBRARY_PATH=/usr/lib:$ORACLE_HOME/lib
$ export PATH=$ORACLE_HOME/bin:$PATH  
```

![image-20200831094804509](E:\Documents\Oracle11g常用管理查询.assets\image-20200831094804509.png)



# 管理控制文件

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