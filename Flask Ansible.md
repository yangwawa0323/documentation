# Flask Ansible





## Ansible 课程简介

Ansible是一个IT工程师的利器，对比其他同类自动化工具，Ansible具有着简易的配置，无需过多的配置每一台客户机和服务器。换句话而言，“去中心化”或者说“没有中心服务器”！Ansible同时具有着丰富的模块涵盖了AWS，Cisco，IBM等各种云或者设备。

通过下面的课程，你将会逐步逐步的了解运维工程师Ansible自动化运维的操作和知识延伸，轻松管理数以百计甚至更多的服务器。

* Ansible的架构
* 配置Ansible
* 配置管理
* 使用 Playbook
* 变量和它的类型
* 使用Inventory 仓库文件
* 使用模块





## 起步

### Ansible 工作原理

Ansible它运行在 Push 模式。它通过SSH协议**Paramiko** Python开发库多线程的方式连接预先配置好的服务器，在服务器端注入执行的Python程序，具体执行的任务是由管理人员提前配置在管理主机上，而非在每天被管理的服务器端。如下图：



![Ansible Working Model](Flask%20Ansible.assets/Ansible%20Working%20Model.png)



### Ansible 的安装

如果在 Linux 下安装 Ansible 极为简单

```shell
$ apt-get install apt-add-repository
$ apt-add-repository ppa:rquillo/ansible
$ apt-get update
$ apt-get install ansible
```



也可以利用 **Github** 源码安装

1. 首先下载源码

```shell
$ git clone git://github.com/ansible/ansible.git
Cloning into 'ansible'...
remote: Enumerating objects: 553575, done.
remote: Counting objects: 100% (556/556), done.
remote: Compressing objects: 100% (388/388), done.
remote: Total 553575 (delta 251), reused 352 (delta 132), pack-reused 553019
Receiving objects: 100% (553575/553575), 185.88 MiB | 3.93 MiB/s, done.
Resolving deltas: 100% (371362/371362), done.
Checking connectivity... done.
```

	2. 切入到Ansible源码下载目录后，设置环境变量

```shell
$ source hacking/env-setup
Ansible now needs setuptools in order to build. Install it using your package manager (usually python-setuptools) or via pip (pip install setuptools).

Setting up Ansible to run out of checkout...

PATH=/root/ansible/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
PYTHONPATH=/root/ansible/lib
MANPATH=/root/ansible/docs/man:/usr/local/man:/usr/local/share/man:/usr/share/man

Remember, you may wish to specify your host file with -i

Done!
```

3. Ansible 需要提前安装一些Python包 **paramiko PyYAML jinja2 httplib2（**这里使用的Python3环境）

```shell
# python3.5
$ curl -fsSL -o- https://bootstrap.pypa.io/pip/3.5/get-pip.py | python3.5
# python3.6+ 
$ apt-get install libssl-dev zlib1g-dev libyaml-dev
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
$ python3.9 get-pip.py
$ pip3 install --upgrade pip
$ pip3 install -r requirements.txt

```

> 注意：由于代码中使用到 **f""** 语法，这一语法是python 3.6+ 才出现的格式化字符串的语法，因此建议将系统的Python 升级到最新稳定版 
>
> 如果继续使用 python3.5 可能你需要创建软链接



```shell
$ ln -s /usr/bin/python3.5 /usr/bin/python
```

​	4.最后检查下Ansible是否安装正常

```shell
$ ansible --version
[DEPRECATION WARNING]: Ansible will require Python 3.8 or newer on the controller starting with
Ansible 2.12. Current version: 3.5.2 (default, Jan 26 2021, 13:30:48) [GCC 5.4.0 20160609]. This
feature will be removed from ansible-core in version 2.12. Deprecation warnings can be disabled by
setting deprecation_warnings=False in ansible.cfg.
/root/ansible/lib/ansible/parsing/vault/__init__.py:44: CryptographyDeprecationWarning: Python 3.5 support will be dropped in the next release of cryptography. Please upgrade your Python.
  from cryptography.exceptions import InvalidSignature
[WARNING]: You are running the development version of Ansible. You should only run Ansible from
"devel" if you are modifying the Ansible engine, or trying out features under development. This is a
rapidly changing source of code and can become unstable at any point.
ansible [core 2.12.0.dev0]  (devel 7ca5dede97) last updated 2021/04/25 08:53:08 (GMT +800)
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /root/ansible/lib/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /root/ansible/bin/ansible
  python version = 3.5.2 (default, Jan 26 2021, 13:30:48) [GCC 5.4.0 20160609]
  jinja version = 2.11.3
  libyaml = False
```

> **墙裂建议**直接安装python3.9 环境，python3.5 不支持 ansible-core



如果你的主机上还存在其他的Python开发环境，为了不会出现包依赖版本混乱现象，我们可以通过Python Virtual Environment运行Ansible

虚拟环境的安装

```shell
$ apt-get install python3-env
$ python3 -m venv venv
$ source venv/bin/activate
$ venv/bin/pip3.8 install ansible
Collecting ansible
  Downloading ansible-3.3.0.tar.gz (31.5 MB)
     |████████████████████████████████| 31.5 MB 60 kB/s

```



### 小试牛刀

编写一个仓库文件 inventory，列入你要管理的主机，如下

```shell
$ cat inventory
[servers]
192.168.2.201
192.168.2.202
```

接着测试一个最为简单的模块 ping 

```shell
$ ansible servers -m ping -i inventory
[WARNING]: You are running the development version of Ansible. You should only run Ansible from
"devel" if you are modifying the Ansible engine, or trying out features under development. This is a
rapidly changing source of code and can become unstable at any point.
192.168.2.202 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
192.168.2.201 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: root@192.168.2.201: Permission denied (publickey,password).",
    "unreachable": true
}
```

> 如果你的结果和这不一致，不用急，我们会在后续的课程中告诉大家原因

再来测试一个常用模块吧

```shell
$ ansible servers -m shell -a '/bin/echo "Hello world"'  -i inventory               
[WARNING]: You are running the development version of Ansible. You should only run Ansible from
"devel" if you are modifying the Ansible engine, or trying out features under development. This is a
rapidly changing source of code and can become unstable at any point.
192.168.2.202 | CHANGED | rc=0 >>
Hello world
192.168.2.201 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: root@192.168.2.201: Permission denied (publickey,password).",
    "unreachable": true
}                                                                                                                  
```

> 两次结果都以192.168.2.201失败告终，这是因为我们以默认账户root登录的原因，而192.168.2.201服务器上出于安全的考虑，ssh连接禁止root用户直接登录。请继续学习。



### 配置 Ansible.cfg

Ansible 的配置文件，你可以灵活的使用，它有四处可供设置的地方，按照尝试查找次序，由高到低排列如下：

1. ANSIBLE_CONFIG 环境变量
2. ./ansible.cfg
3. ~/.ansible.cfg
4. /etc/ansible/ansible.cfg

>  如果你是通过 **github** 源码下载，在 examples 目录下有着所有选项全被注释的模板配置文件



### 常用的几个配置选项

* hostfile

* library

* forks

* sudo_user

* remote_port

* host_key_checking

* timeout

* log_path

  

### 小试 playbook

playbooks/setup_apache.yaml

```yaml
#!/usr/bin/env ansible-playbook
---
#
- hosts: all
  gather_facts: yes
  connection: ssh
  become: True
  tasks:
     - name: Install httpd package
       apt:
          name: apache2
          state: latest

     - name: Starting httpd service
       service: name=apache2 state=started
 
```



* 列举任务 **--list-tasks**

```shell
$ ansible-demo# ansible-playbook -i inventory playbooks/setup_apache.yaml --list-tasks
```

* 执行某一段开始以及其后的任务 **--start-at**

```shell
$ ansible-playbook -i inventory playbooks/setup_apache.yaml --start-at 'Install httpd package'
PLAY [all] **********************************************************************

TASK [Gathering Facts] **********************************************************ok: [192.168.2.202]
ok: [192.168.2.201]

TASK [Install httpd package] ****************************************************[WARNING]: Updating cache and auto-installing missing dependency: python-apt
fatal: [192.168.2.202]: FAILED! => {"changed": false, "cmd": "apt-get update", "msg": "[Errno 2] No such file or directory", "rc": 2, "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
ok: [192.168.2.201]

TASK [Starting httpd service] ***************************************************ok: [192.168.2.201]

PLAY RECAP **********************************************************************192.168.2.201              : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.2.202              : ok=1    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```

> 注意：start-at 其后的任务都会被执行

* 问答交互式 **--step**

```shell
$ ansible-playbook -i inventory playbooks/setup_apache.yaml --start-at 'Starting httpd service' --step
[WARNING]: You are running the development version of Ansible. You should only
run Ansible from "devel" if you are modifying the Ansible engine, or trying out
features under development. This is a rapidly changing source of code and can
become unstable at any point.

PLAY [all] **********************************************************************Perform task: TASK: Gathering Facts (N)o/(y)es/(c)ontinue: n

Perform task: TASK: Gathering Facts (N)o/(y)es/(c)ontinue: **********************Perform task: TASK: Starting httpd service (N)o/(y)es/(c)ontinue: y

Perform task: TASK: Starting httpd service (N)o/(y)es/(c)ontinue: ***************

TASK [Starting httpd service] ***************************************************ok: [192.168.2.201]
fatal: [192.168.2.202]: FAILED! => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python"}, "changed": false, "msg": "Could not find the requested service apache2: host"}

PLAY RECAP **********************************************************************192.168.2.201              : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.2.202              : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

```



## 变量和类型

变量用于存储值以便以后在playbook中的其他地方使用。它可以是提前设置也可以是运行模块后覆盖而来。

* **set-fact** 常用于对远程**被管理**的主机信息收集后的变量设置

playbook/vars.yaml

```yaml
- set_fact： package_name=httpd
  when: ansible_os_family == "Redhat"
  
- set_fact： package_name=apache2
  when: ansible_os_family == "Debian"
```

* **register** 常用于**管理端**注册变量

```yaml
- name: Package to install
  pause: prompt="Provide the package name which you want to install"
  register: package_name
```

* 还可以保存在列表中循环的调用每一个变量(详见后)



> 提示：如果多个 playbook 都用相同的变量，为了减少冗余性，避免一个一个的修改，我们还可以将变量放在一个变量文件中，通过引用变量文件的方式调用

假设你运维的环境多种版本的Linux共存，对Redhat/CenterOS而言 Apache的包名为*httpd*, 而Debian/Ubuntu系统则称呼为*apache2*,我们可以依据上面的 playbook/vars.yaml 中的定义选择安装

```yaml
---
#
- hosts: all
  gather_facts: yes
  connection: ssh
  become: True
  tasks:
     - include: ./vars.yaml

     - name: Install httpd package
       apt:
          name: "{{ package_name }}"
          state: latest
       # become: True

     - name: Starting httpd service
       service: name="{{ package_name }}" state=started
       # become: True
```

> 注：首先通过 **include** 将变量文件引用进来
>
> ​        此处用到 "{{}}" 这是雷同于 Django/Flask 一样采用的 Jinjia2 模板的插值表达式，将变量插入双层花括号中。
>
> ​		模板插值表达式本身是一种字符串，因此要写入双引号中。

> 踩坑注意：很多次测试中，我本人都写错了 ansible_os_family == "Redhat" 造成执行有误， 原因在于 **"RedHat"** 。
>
> 为了确保收集信息的正确性，最好是提前运行调用 **setup 模块**命令，然后复制粘贴





```shell
$ ansible -m setup -i inventory 192.168.2.202

192.168.2.202 | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "192.168.2.202"
        ],
        "ansible_all_ipv6_addresses": [
            "fe80::20c:29ff:fe12:5837"
        ],
        "ansible_apparmor": {
            "status": "disabled"
        },
        "ansible_architecture": "x86_64",
        "ansible_bios_date": "07/22/2020",
        "ansible_bios_vendor": "Phoenix Technologies LTD",
        "ansible_bios_version": "6.00",
        "ansible_board_asset_tag": "NA",
        "ansible_board_name": "440BX Desktop Reference Platform",
        "ansible_board_serial": "None",
        "ansible_board_vendor": "Intel Corporation",
        "ansible_board_version": "None",
        "ansible_chassis_asset_tag": "No Asset Tag",
        "ansible_chassis_serial": "None",
        "ansible_chassis_vendor": "No Enclosure",
        "ansible_chassis_version": "N/A",
        "ansible_cmdline": {
            "BOOT_IMAGE": "/vmlinuz-3.10.0-327.el7.x86_64",
            "LANG": "en_US.UTF-8",
            "quiet": true,
            "rd.lvm.lv": "centos/swap",
            "rhgb": true,
            "ro": true,
            ...
```







变量名的命名建议使用单词加上下划线**断词**的方式，以下都为错误的演示：

```
mysql version
mysql.port
5
user-input
```



### 变量全局文件

在Ansible中也可以定义成单独的一个文件，这样方便从playbook中分离数据。你可以任意的定义多个变量全局文件。比如编写一个 *playbook/global.yaml*

```yaml
---
package_name:"httpd"

# Environment variables
mount_point: "/dev/sdf"
```

这样就可以通过 **vars_files** 以列表形式引入

```yaml
---
- hosts: all
  remote_user: oracle
  vars_files:
    - var1.yaml
    - var2.yaml
    - global.yaml
  
  tasks:
    - name: Check apache service
      service: name="{{ package_name }}" state=started
      become: True
```

> 注意：vars_files 提供多个全局文件，当找一个变量时，会由上至下查找，一旦找到跳出查询过程，因此全局文件是讲求次序的。



### facts 作为变量

```shell
$ ansible 192.168.2.202 -i inventory -m setup
 "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "192.168.2.201"
        ],
        "ansible_all_ipv6_addresses": [
            "fe80::20c:29ff:fe2e:935d"
        ],
        "ansible_apparmor": {
            "status": "enabled"
        },
        "ansible_architecture": "x86_64",
        "ansible_bios_date": "07/22/2020",
        "ansible_bios_vendor": "Phoenix Technologies LTD",
        "ansible_bios_version": "6.00",
        "ansible_board_asset_tag": "NA",
        "ansible_board_name": "440BX Desktop Reference Platform",
        "ansible_board_serial": "NA",
        ...
```



### 命令行变量

你可以在命令行中使用额外的变量，通过 --extra-vars 

```shell
$ ansible-playbook -i inventory playbook/apache.yaml \
  --extra-vars "package_name=apache2"
```



## 使用仓库文件

仓库文件是最直观的反映被管理的主机信息的。它是 **INI** 文件格式。Ansible可以使用多线程形式同时操作多台主机。Ansible可以让你对你的主机在仓库分组存放。当操作组名时，Ansible将针对此组的所有主机执行相同任务。

> 缺省，所有的主机隶属于一个隐性的组**all**



#### 基本仓库文件

将所有要管理的主机列入文件就成了基本仓库文件

```ini
example.com
web001
51cloudclass.com
db001
192.168.2.201
192.168.2.202
```



####　分组仓库文件

采用分组的原因是因为在日常管理主机时，我们需要套用一些列规则给具有相同功能的主机，比如检查负载均衡架构下的数十台Web功能的服务器Nginx运行状态...

```ini
[application]
example.com
db001
[exam]
192.168.2.201
192.168.2.202
[webserver]
51cloudclass.com
web001
```

定义好组，我们在playbook中就可以直接使用组名称

```yaml
---
- hosts: webserver
  remote_user: oracle
  vars_files:
    - global.yaml
  
  tasks:
    - name: Check apache service
      service: name="{{ package_name }}" state=started
      become: True
```



#### 组上组-超组

对分组还可以再次分组，这里我们用到一个关键字**children**，用冒号"**:**"分割，比如分组之后还需要按照架构的地区或者机架归类

```ini
[application]
example.com
db001
[exam]
192.168.2.201
192.168.2.202
[webserver]
51cloudclass.com
web001

[east:children]
application
webserver
```

> 由上例可以看到超组*east*，其中的信息就为application和webserver两个组，这样就不要复制这两个组的主机合成一个新的组这样冗余的操作了。



#### 正则表达式的应用

如果服务器规划是有规律的命名，还可以用正则表示代表连续的主机

```ini
[database]
db001
db[002:199]
```

> 上例中 db[002:199] 将等价于 db002, db003, ..., db199 的主机

-------



#### 主机变量

仓库文件还可以传递Ansible变量给 playbook

```
[database]
db001 db_name=redis db_port=6380

```



#### 组变量

同样的道理，一个管理员管理的主机基本具有相同的基因，组中的主机参数设置一致，比如端口，账户之类的。为了省去复制粘贴重复再重复的操作。在主机分组配置完之后再次使用组名称加一个关键字 **vars**，为分组中所有的主机设置变量

```ini
[database]
example.com
db001
[exam]
192.168.2.201
192.168.2.202
[webserver]
51cloudclass.com
web001

[database:vars]
db_name=redis
db_port=16380

```



#### 可覆盖的配置参数

前面我们介绍了ansible.cfg配置文件，其中有着很多的配置参数，在仓库文件中也可以覆盖使用。下面罗列几个常用连接的参数

* ansible_ssh_user
* ansible_ssh_port
* ansible_ssh_host
* ansible_ssh_private_key_file

```ini
[database]
example.com ansible_ssh_port=10022
db001 ansible_ssh_user=oracle ansible_ssh_private_key=myuser.rsa
```



## 使用模块

Ansible 具有着差不多 200+ 的模块，足以应对日常的复杂运维管理。AWS，HP，Cisco，IBM等大厂商更加对自身旗下的产品开发了开源的管理模块。因此 Ansible 涉及到系统，网络设备，数据库，文件，刀片服务器







## 使用 tag 标签

如同网页信息中呈现的关键字一样。给任务赋予标签，我们可以基于此标签执行单个或成批的任务。一个任务可以赋予多个标签，同样一个标签可是设置在多个任务之上，这样形成M对N的笛卡尔交集的管理方式。

*playbook/tags_example.yaml*

```yaml
---
#
- hosts: all
  become: True
  tasks:
     - include: ./vars.yaml

     - name: Install httpd package
       apt:
          name: "{{ package_name }}"
          state: latest
       tags:
         - install

     - name: Starting httpd service
       service: name="{{ package_name }}" state=started
       tags:
         - start
         
     - name：Starting vsftpd service
       service: name=vsftpd state=started
       tags:
         - start
```

而在我们调用 **ansible-playbook** 命令时，使用 **--tags** 参数

```shell
$ ansible-playbook -i inventory playbook/tags_example.yaml --tags start
```

这样同时启动 *vsftpd* 和 *apache2* 服务，因为 playbook 中有两个任务有着 **start** 标签。

> 相比之前的 **--start-at** 只能从某个任务开始执行其后的所有任务，标签给我们带来的是更多的弹性选择。

如果同时执行多个标签，简单的用逗号  "**，**"  间隔标签即可

```shell
$ ansible-playbook -i inventory playbook/tags_example.yaml --tags pre_check,start
```

相反如果要鸡蛋里挑骨头，我们可以通过 --skip-tags ，排除执行某种标签的任务，转而执行剩下的其他任务

```shell
$ ansible-playbook -i inventory playbook/tags_example.yaml --skip-tags install,stop
```



#### group_vars 目录

为了将 Inventory 仓库文件最小化，我们还可以将分组文件单独的放置在一个目录下，这个目录就是和仓库文件相同目录下建立一个group_vars, 然后以分组的名称建立单个的变量文件，比如 webserver 分组就创建 webserver 的变量文件

```shell
$ tree
.
├── group_vars
│   └── servers
├── inventory
└── playbooks
    ├── apache.yaml
    ├── setup_apache.yaml
    └── vars.yaml
```



## local_action



## Ansible中条件判断



* debug
* when
  * is not defined
  * is defined

```yaml
- name: Checking backup path
  pause: prompt="Please provide a path for backup"
  register: backup_path
  when: backup_path is not defined

- name: Rsync the entire disk
  shell: /usr/bin/rsync -ra / {{ backup_path.user_input }} --exclude='/proc' --exclude='/sys' -exclude='/backup'
  become: True
  when: backup and backup_path is defined
```



* fail

  

## Ansible 中循环

### 标准循环

with_items

### 内嵌循环

with_nested

### 循环变量中的子元素

```yaml
---
- hosts: web001
  remote_user: oracle
  vars:
    users:
      - name: alice
        database:
          - clientdb
          - employeedb
          - providerdb
      - name: bob
        database:
          - clientdb
          
  tasks:
    - name: give users access to multiple databases
      #mysql_user: name={{ item.0.name }} priv={{ item.1 }}.*:ALL append_privs=yes password=foo login_user=root login_password=password
      debug: msg="name={{ item.0.name }} priv={{ item.1 }}.*:ALL append_privs=yes password=foo login_user=root login_password=password"
      with_subelements:
        - "{{ users }}"
        - database
```

> 注意：
>
> ​       上例中 with_subelements 的第一个元素使用 template 语法 "{{ user }}" 因为它是包裹在最外层的元素。
>
> 理解：
>
> ​      为什么一会写 item.0 ， 一会 item.1？
>
> ​      此时的 item 是相对于 with_subelements 而言，在此例中 item.0 也就是通过template语法插值表达式的 users 变量。而 item.1就对应为 database，**此处很重要**，我们并没有定义database变量。其实subelements的意思是子元素也就是嵌套的元素意思。因此此处的 database实际上是 users 变量中其中一个元素的内部叫做database的属性。到此为止，我们推导出来 **item.1 == item.0.*database***, "0"作为"1" 的**上一级**，转换成**父级**, 总结： 0作为外层循环，1最为0内部的内层循环。注意**没有 item.2** 的出现，因为**for for for 三层循环**本身在程序中就要避免出现。
>
> ​    结合报错信息和源代码分析：with_subelements 的**第三个元素只可能是 skip_missing: True** 这个字典对象，代表前两层元素如果缺失将跳过

结合上面的运行结果输出再仔细看看吧：

```shell
$ ansible-playbook -i inventory ./playbooks/with_subelements_demo.yaml
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are
modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

PLAY [demo_group1] ***************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************ok: [192.168.2.201]

TASK [set_fact] ******************************************************************************************************skipping: [192.168.2.201]

TASK [set_fact] ******************************************************************************************************ok: [192.168.2.201]

TASK [give users access to multiple databases] ***********************************************************************ok: [192.168.2.201] => (item=[{'name': 'alice'}, 'clientdb']) => {
    "msg": "name=alice priv=clientdb.*:ALL append_privs=yes password=foo login_user=root login_password=password"
}
ok: [192.168.2.201] => (item=[{'name': 'alice'}, 'employeedb']) => {
    "msg": "name=alice priv=employeedb.*:ALL append_privs=yes password=foo login_user=root login_password=password"
}
ok: [192.168.2.201] => (item=[{'name': 'alice'}, 'providerdb']) => {
    "msg": "name=alice priv=providerdb.*:ALL append_privs=yes password=foo login_user=root login_password=password"
}
ok: [192.168.2.201] => (item=[{'name': 'bob'}, 'clientdb']) => {
    "msg": "name=bob priv=clientdb.*:ALL append_privs=yes password=foo login_user=root login_password=password"
}

PLAY RECAP ***********************************************************************************************************192.168.2.201              : ok=3    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0


```





### 使用 Include 引用文件

### 使用 handler 触发事件

在很多场景中，你需要一个任务或者一组任务在远程主机上执行修改资源，当Ansible确认这些变化后，这一事件**触发**下一个任务。比如说当包或应用程序的配置文件修改，你将需要重启相关的服务。

**Ansible** 提供了一个 **notify** 的指令 和 一个 **handlers** 属性的定义。**handlers** 原则上格式和 **tasks** 一模一样，不过它执行的条件就只有 **notify** 其中**对应的任务名称**。

下面我们来看个范例

```yaml
---
- hosts: demo_group1
  remote_user: oracle
  tasks:
    - name: Create a virtual host
      template: src=http_test.conf_web dest=/etc/httpd/conf/test.conf mode=0644 validate='httpd -t -f %s'
      become: True
      notify:
        - restart httpd
   
  handlers:
    - name: restart httpd
      service: name=httpd state=restarted
      become: True
```

> 注意： 很多时候事件触发后续任务的执行，错就错在 notify 通知的**任务名称有出入**，包括空格数量，大小写字母。建议鼠标复制 handlers 中对应的任务名称粘贴到 notify 处。

> 注意：还有一点是只有远程主机执行对应的任务**发生了变化** "**changed**", 才会有 notify 事件 。否则没有必要去执行对应的后续任务，正如之前所描述一样，如果Apache配置文件没有发生过变化根本不需要去重启 httpd 服务。

> 提示：handlers 同样支持 include 形式

```yaml
- handlers:
    - include: handlers.yaml

```



### 使用 Role 角色

当你的 playbook 中 include 日趋居多甚至膨胀增长，或者你有着大量的模板，这时你需要使用 Ansible 中的角色功能。

Ansible 中角色功能可以让你按照目录夹的结构分组文件。每一个角色一个目录，在角色目录夹下又具有着相同的子目录 variables, files, tasks, templates, handlers。

而在定义规则文件中，只需使用 roles 列表就可以实现雷同于 include 一样的各种引用。

```shell
root@DESKTOP-08E761I:ansible-demo# tree
.
├── group_vars
│   └── servers
├── inventory
├── playbooks
│   ├── apache.yaml
│   ├── setup_apache.yaml
│   ├── vars.yaml
│   └── with_subelements_demo.yaml
└── roles
    ├── database
    │   ├── README.md
    │   ├── defaults
    │   │   └── main.yml
    │   ├── files
    │   ├── handlers
    │   │   └── main.yml
    │   ├── meta
    │   │   └── main.yml
    │   ├── tasks
    │   │   └── main.yml
    │   ├── templates
    │   ├── tests
    │   │   ├── inventory
    │   │   └── test.yml
    │   └── vars
    │       └── main.yml
    └── webserver
        ├── README.md
        ├── defaults
        │   └── main.yml
        ├── files
        ├── handlers
        │   └── main.yml
        ├── meta
        │   └── main.yml
        ├── tasks
        │   └── main.yml
        ├── templates
        ├── tests
        │   ├── inventory
        │   └── test.yml
        └── vars
            └── main.yml
```

正如上面目录结构，每个目录下缺省入口文件为 **main.yml**,可以在 main.yml 再用 **include** 语法包含自身目录下的其他配置文件

考虑到创建角色的目录过于复杂，Ansible 后续提供了一条 **ansible-galaxy** 命令，带入参数就可以初始化角色的目录

```shell
$ ansible-galaxy role --help
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are
modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.
usage: ansible-galaxy role [-h] ROLE_ACTION ...

positional arguments:
  ROLE_ACTION
    init       Initialize new role with the base structure of a role.
    remove     Delete roles from roles_path.
    delete     Removes the role from Galaxy. It does not remove or alter the actual GitHub repository.
    list       Show the name and version of each role installed in the roles_path.
    search     Search the Galaxy database by tags, platforms, author and multiple keywords.
    import     Import a role into a galaxy server
    setup      Manage the integration between Galaxy and the given source.
    info       View more details about a specific role.
    install    Install role(s) from file(s), URL(s) or Ansible Galaxy

optional arguments:
  -h, --help   show this help message and exit

$ cd roles
$ ansible-galaxy role init database
```

最后要怎样设置任务中的角色了？

我们通过在任务中设定 roles 列表即可自动查找对应角色目录下的所有的配置文件

```yaml

---
- name: Setup servers for website1.example.com
  hosts: website1
  roles:
    - common
    - apache
    - { role: website1, port: 80 }
```

> 注意：上例中Ansible任务如何扮演 common 角色的了？
>
> 首先，Ansible 将尝试加载 roles/*common*/**tasks**/**main**.yml 做为任务的引用，roles/*common*/**handlers**/**main**.yml  做为处罚事件的引用，roles/common/vars/main.yml 做为变量的引用。如果上述三个文件都不存在，Ansible 将抛出一个错误。任何其一存在将会加载，缺失的将忽略。

> 注意：最后的 { **role**: website1, *port: 80* } 代表着原则上扮演 *website1* 的角色，但是单独设置了一个端口为80的变量，如果在角色的变量文件中定义过此变量的缺省值，这里的定义将最终覆盖缺省值。换句话：最后这条就是稍微的个性化设置 。





## Ansible 模板

[过滤器](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html)

### 格式化数据

{{ user | to_nice_json }}

{{ user | to_nice_yaml }}

###　条件判断中使用过滤器

你可以使用 Jinja2过滤条件判断，检查一个任务执行的状态 

* failed
* changed
* success
* skipped

如下面的例子

```yaml
- name: Checking httpd service
  service: name=httpd state=running
  register: httpd_result
  ignore_errors: True
  
- name: Debuging httpd service state
  debug: msg="Previous task failed"
  when: httpd_result|failed
```

> 注意：Ansible 较低的版本仍采用过滤器对进行条件判断，2.9+以上改为了**"is" 判断**,而没有用过滤器
>
> when: httpd_result is failed

```yaml
#!/usr/bin/env ansible-playbook
---
#
- hosts: demo_group1
  gather_facts: yes
  connection: ssh
  become: True
  tasks:
     - include: vars.yaml


     - name: Starting httpd service
       service: name="{{ package_name }}" state=started
       # become: True
       register: httpd_state
       tags:
         - start

     - name: Debug httpd failed status
       debug: msg="Previous {{ package_name }} failed"
       when: httpd_state is failed

     - name: Debug httpd success status
       debug: msg="Previous {{ package_name }} success"
       when: httpd_state is success

     - name: Debug httpd skipped status
       debug: msg="Previous {{ package_name }} skipped"
       when: httpd_state is skipped
```

### 默认值

default()



## ansible-vault 密码保护

```shell
$ ansible-vault --help
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are
modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.
usage: ansible-vault [-h] [--version] [-v] {create,decrypt,edit,view,encrypt,encrypt_string,rekey} ...

encryption/decryption utility for Ansible data files

positional arguments:
  {create,decrypt,edit,view,encrypt,encrypt_string,rekey}
    create              Create new vault encrypted file
    decrypt             Decrypt vault encrypted file
    edit                Edit vault encrypted file
    view                View vault encrypted file
    encrypt             Encrypt YAML file
    encrypt_string      Encrypt a string
    rekey               Re-key a vault encrypted file

optional arguments:
  --version             show program's version number, config file location, configured module search path, module
                        location, executable location and exit
  -h, --help            show this help message and exit
  -v, --verbose         verbose mode (-vvv for more, -vvvv to enable connection debugging)

See 'ansible-vault <command> --help' for more information on a specific command.

root@DESKTOP-08E761I:ansible-demo# ansible-vault create --help
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are
modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.
usage: ansible-vault create [-h] [--encrypt-vault-id ENCRYPT_VAULT_ID] [--vault-id VAULT_IDS]
                            [--ask-vault-password | --vault-password-file VAULT_PASSWORD_FILES] [-v]
                            [file_name [file_name ...]]

positional arguments:
  file_name             Filename

optional arguments:
  -h, --help            show this help message and exit
  --encrypt-vault-id ENCRYPT_VAULT_ID
                        the vault id used to encrypt (required if more than one vault-id is provided)
  --vault-id VAULT_IDS  the vault identity to use
  --ask-vault-password, --ask-vault-pass
                        ask for vault password
  --vault-password-file VAULT_PASSWORD_FILES, --vault-pass-file VAULT_PASSWORD_FILES
                        vault password file
  -v, --verbose         verbose mode (-vvv for more, -vvvv to enable connection debugging)
```



```shell
```



------

## Ansible API

### DataLoader

**ansible.parsing.dataloader.DataLoader()**



### InventoryManger

```python
def get_play_prereqs_2_4(self, options):
        loader = DataLoader()

        if self.vault_pass:
            loader.set_vault_secrets([('default', VaultSecret(_bytes=to_bytes(self.vault_pass)))])

        # create the inventory, and filter it based on the subset specified (if any)
        inventory = InventoryManager(loader=loader, sources=options.inventory)

        # create the variable manager, which will be shared throughout
        # the code, ensuring a consistent view of global variables
        try:
            # Ansible 2.8
            variable_manager = VariableManager(loader=loader, inventory=inventory,
                                               version_info=self.version_info(ansible_version))
            variable_manager._extra_vars = self.extra_vars
        except TypeError:
            variable_manager = VariableManager(loader=loader, inventory=inventory)
            variable_manager.extra_vars = self.extra_vars
            variable_manager.options_vars = {'ansible_version': self.version_info(ansible_version)}

        return loader, inventory, variable_manager 
```

```python
def ansible_part():
    playbook_path = "checktemplate.yml"
    inventory_path = "hosts"

    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff', 'listhosts', 'listtasks', 'listtags', 'syntax'])
    loader = DataLoader()
    options = Options(connection='local', module_path='', forks=100, become=None, become_method=None, become_user=None, check=False,
                    diff=False, listhosts=False, listtasks=False, listtags=False, syntax=False)
    passwords = dict(vault_pass='secret')

    inventory = InventoryManager(loader=loader, sources=['inventory'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    executor = PlaybookExecutor(  
                playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader,  
                options=options, passwords=passwords)  
    results = executor.run()  
    print results 
```



### VariableManager

```python
def parse_inventory(inventory):
    loader = DataLoader()
    inv = InventoryManager(loader=loader, sources=[inventory])
    vars = VariableManager(loader=loader, inventory=inv)
    all_groups = inv.get_groups_dict()
    tidb_nodes = all_groups['tidb_servers']
    tikv_nodes = all_groups['tikv_servers']
    tidb_servers = {}
    tikv_servers = {}
    for tidb in tidb_nodes:
        var = vars.get_vars(host=inv.get_host(hostname=str(tidb)))
        ip = var['ansible_host'] if 'ansible_host' in var else var['inventory_hostname']
        tidb_port = var.get('tidb_port', 4000)
        tidb_status_port = var.get('tidb_status_port', 10080)
        deploy_dir = var['deploy_dir']

        if ip in tidb_servers:
            tidb_servers[ip].append([tidb_port, tidb_status_port, deploy_dir])
        else:
            tidb_servers[ip] = [[tidb_port, tidb_status_port, deploy_dir]]

    for tikv in tikv_nodes:
        var = vars.get_vars(host=inv.get_host(hostname=str(tikv)))
        ip = var['ansible_host'] if 'ansible_host' in var else var['inventory_hostname']
        tikv_port = var.get('tikv_port', 20160)
        tikv_status_port = var.get('tikv_status_port', 20180)
        deploy_dir = var['deploy_dir']

        if ip in tikv_servers:
            tikv_servers[ip].append([tikv_port, tikv_status_port, deploy_dir])
        else:
            tikv_servers[ip] = [[tikv_port, tikv_status_port, deploy_dir]]

    return [tidb_servers, tikv_servers] 
```



### PlaybookExecutor

```python
def execute_playbook():
    playbook_path = "playbook_template.yml"
    inventory_path = "hosts"

    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff', 'listhosts', 'listtasks', 'listtags', 'syntax'])
    loader = DataLoader()
    options = Options(connection='local', module_path='', forks=100, become=None, become_method=None, become_user=None, check=False,
                    diff=False, listhosts=False, listtasks=False, listtags=False, syntax=False)
    passwords = dict(vault_pass='secret')

    inventory = InventoryManager(loader=loader, sources=['inventory'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    executor = PlaybookExecutor(  
                playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader,  
                options=options, passwords=passwords)  
    results = executor.run()  
    print results 
```



```python
# -*- coding:utf-8 -*-

import os
from collections import namedtuple

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.playbook.play import Play
import ansible.constants as C

from .callback import AdHocResultCallback, PlaybookResultCallBack, \
    CommandResultCallback
from .exceptions import AnsibleError


__all__ = ["AdHocRunner", "PlayBookRunner"]
C.HOST_KEY_CHECKING = False


Options = namedtuple('Options', [
    'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
    'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
    'scp_extra_args', 'become', 'become_method', 'become_user',
    'verbosity', 'check', 'extra_vars', 'playbook_path', 'passwords',
    'diff', 'gathering', 'remote_tmp', ])


def get_default_options():
    options = Options(
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        timeout=60,
        connection='ssh',
        module_path='',
        forks=20,
        remote_user='root',
        private_key_file=None,
        ssh_common_args="",
        ssh_extra_args="",
        sftp_extra_args="",
        scp_extra_args="",
        become=None,
        become_method=None,
        become_user=None,
        verbosity=None,
        extra_vars=[],
        check=False,
        playbook_path='/etc/ansible/',
        passwords=None,
        diff=False,
        gathering='implicit',
        remote_tmp='/tmp/.ansible'
    )
    return options

#  执行 yml 文件


class PlayBookRunner:

    # Default results callback
    results_callback_class = PlaybookResultCallBack
    loader_class = DataLoader
    variable_manager_class = VariableManager
    options = get_default_options()

    def __init__(self, playbook_path, inventory=None, options=None):
        """
        :param options: Ansible options like ansible.cfg
        :param inventory: Ansible inventory
        :param BaseInventory:The BaseInventory parameter hostname must be equal to the hosts in yaml
        or the BaseInventory parameter groups must equal to the hosts in yaml.
        """
        if options:
            self.options = options
        C.RETRY_FILES_ENABLED = False
        self.inventory = inventory
        # self.loader = self.loader_class()
        self.loader = DataLoader()
        self.results_callback = self.results_callback_class()
        # self.playbook_path = options.playbook_path
        self.playbook_path = playbook_path
        self.variable_manager = self.variable_manager_class(
            loader=self.loader, inventory=self.inventory
        )
        # self.passwords = options.passwords
        self.passwords = {"passwords": ''}  # 为了修改paramiko中的bug添加入，无实际意义
        self.__check()

    def __check(self):
        if self.options.playbook_path is None or \
                not os.path.exists(self.options.playbook_path):
            raise AnsibleError(
                "Not Found the playbook file: {}.".format(
                    self.options.playbook_path))
        if not self.inventory.list_hosts('all'):
            raise AnsibleError('Inventory is empty')

    def run(self):
        executor = PlaybookExecutor(
            playbooks=[self.playbook_path],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords
        )

        if executor._tqm:
            executor._tqm._stdout_callback = self.results_callback
        executor.run()
        executor._tqm.cleanup()
        try:
            results_callback = self.results_callback.output['plays'][0]['tasks'][1]['hosts']
            status = self.results_callback.output['stats']
            results = {"results_callback": results_callback, "status": status}
            return results
        except Exception as e:

            raise AnsibleError(
                'The hostname parameter or groups parameter in the BaseInventory \
                               does not match the hosts parameter in the yaml file.{}'.format(e))


class AdHocRunner:
    """
    ADHoc Runner接口
    """
    results_callback_class = AdHocResultCallback
    loader_class = DataLoader
    variable_manager_class = VariableManager
    options = get_default_options()
    default_options = get_default_options()

    def __init__(self, inventory, options=None):
        if options:
            self.options = options
        self.inventory = inventory
        self.loader = DataLoader()
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory
        )

    @staticmethod
    def check_module_args(module_name, module_args=''):
        if module_name in C.MODULE_REQUIRE_ARGS and not module_args:
            err = "No argument passed to '%s' module." % module_name
            raise AnsibleError(err)

    def check_pattern(self, pattern):
        if not pattern:
            raise AnsibleError("Pattern `{}` is not valid!".format(pattern))
        if not self.inventory.list_hosts("all"):
            raise AnsibleError("Inventory is empty.")
        if not self.inventory.list_hosts(pattern):
            raise AnsibleError(
                "pattern: %s  dose not match any hosts." % pattern
            )

    def clean_tasks(self, tasks):
        cleaned_tasks = []
        for task in tasks:
            self.check_module_args(
                task['action']['module'],
                task['action'].get('args'))
            cleaned_tasks.append(task)
        return cleaned_tasks

    def set_option(self, k, v):
        kwargs = {k: v}
        self.options = self.options._replace(**kwargs)

    def run(
            self,
            tasks,
            pattern,
            play_name='Ansible Ad-hoc',
            gather_facts='no',):
        """
        :param gather_facts:
        :param tasks: [{'action': {'module': 'shell', 'args': 'ls'}, ...}, ]
        :param pattern: all, *, or others
        :param play_name: The play name
        :return:
        """
        self.check_pattern(pattern)
        results_callback = self.results_callback_class()
        cleaned_tasks = self.clean_tasks(tasks)

        play_source = dict(
            name=play_name,
            hosts=pattern,
            gather_facts=gather_facts,
            tasks=cleaned_tasks
        )

        play = Play().load(
            play_source,
            variable_manager=self.variable_manager,
            loader=self.loader,
        )

        tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            stdout_callback=results_callback,
            passwords=self.options.passwords,
        )

        try:
            tqm.run(play)
            return results_callback
        except Exception as e:
            raise AnsibleError(e)
        finally:
            tqm.cleanup()
            self.loader.cleanup_all_tmp_files()


class CommandRunner(AdHocRunner):
    results_callback_class = CommandResultCallback
    modules_choices = ('shell', 'raw', 'command', 'script')

    def execute(self, cmd, pattern, module=None):
        if module and module not in self.modules_choices:
            raise AnsibleError(
                "Module should in {}".format(
                    self.modules_choices))
        else:
            module = "shell"

        tasks = [
            {"action": {"module": module, "args": cmd}}
        ]
        hosts = self.inventory.get_hosts(pattern=pattern)
        name = "Run command {} on {}".format(
            cmd, ", ".join([host.name for host in hosts]))
        return self.run(tasks, pattern, play_name=name)
```





test_runner.py

```python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0,"../..")
import json
from tasks.ansible.runner import AdHocRunner,CommandRunner,PlayBookRunner
from tasks.ansible.inventory import BaseInventory




def  TestAdHocRunner():
        """
         以yml的形式 执行多个命令
        :return:
        """

        host_data = [
            {
                "hostname": "192.168.10.102",
                "ip": "192.168.10.102",
                "port": 22,
                "username": "root",
                "password": "123456",
            },
        ]
        inventory = BaseInventory(host_data)
        runner = AdHocRunner(inventory)

        tasks = [
            #{"action": {"module": "cron","args": "name=\"sync time\" minute=\"*/3\" job=\"/usr/sbin/ntpdate time.nist.gov &> /dev/null\"" }, "name": "run_cmd"},
            {"action": {"module": "shell", "args": "ifconfig"}, "name": "run_whoami"},
        ]
        ret = runner.run(tasks, "all")
        print(ret.results_summary)
        print(ret.results_raw)

def TestCommandRunner():
        """
        执行单个命令，返回结果
        :return:
        """

        host_data = [
            {
                "hostname": "192.168.10.102",
                "ip": "192.168.10.102",
                "port": 22,
                "username": "root",
                "password": "123456",
            },
        ]
        inventory = BaseInventory(host_data)
        runner = CommandRunner(inventory)

        #该模块可以运行command，shell，raw，script，直接写入参数即可。
        res = runner.execute('df -h', 'all')
        #res = runner.execute("/root/sayhell.sh", 'all')
        #print(res.results_command)
        res_command = res.results_command
        print('------------')
        print(json.dumps(res_command))

        #print(res.results_raw)
        print('-------------')
        print(json.dumps(res.results_raw))
        #print(res.results_command['10.135.133.214']['stdout'])

if __name__ == "__main__":
    #TestAdHocRunner()
    TestCommandRunner()
```



test_inventory.py

```python
# -*- coding:utf-8 -*-
import sys

sys.path.insert(0,"../..")

from tasks.ansible.inventory import BaseInventory



def  Test():
        """
        返回主机信息，组信息，组内主机信息
        :return:
        """
        host_list = [{
            "hostname": "testserver1",
            "ip": "102.1.1.1",
            "port": 22,
            "username": "root",
            "password": "password",
            "private_key": "/tmp/private_key",
            "become": {
                "method": "sudo",
                "user": "root",
                "pass": None,
            },
            "groups": ["group1", "group2"],
            "vars": {"sexy": "yes"},
        }, {
            "hostname": "testserver2",
            "ip": "8.8.8.8",
            "port": 2222,
            "username": "root",
            "password": "password",
            "private_key": "/tmp/private_key",
            "become": {
                "method": "su",
                "user": "root",
                "pass": "123",
            },
            "groups": ["group3", "group4"],
            "vars": {"love": "yes"},
        }]

        inventory = BaseInventory(host_list=host_list)


        print("#"*10 + "Hosts" + "#"*10)
        for host in inventory.hosts:
            print(host)


        print("#" * 10 + "Groups" + "#" * 10)
        for group in inventory.groups:
            print(group)


        print("#" * 10 + "all group hosts" + "#" * 10)
        group = inventory.get_group('all')
        print(group.hosts)


if __name__ == '__main__':
    Test()
```



test_runner.py

```python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0,"../..")
import json
from tasks.ansible.runner import AdHocRunner,CommandRunner,PlayBookRunner
from tasks.ansible.inventory import BaseInventory




def  TestAdHocRunner():
        """
         以yml的形式 执行多个命令
        :return:
        """

        host_data = [
            {
                "hostname": "192.168.10.102",
                "ip": "192.168.10.102",
                "port": 22,
                "username": "root",
                "password": "123456",
            },
        ]
        inventory = BaseInventory(host_data)
        runner = AdHocRunner(inventory)

        tasks = [
            #{"action": {"module": "cron","args": "name=\"sync time\" minute=\"*/3\" job=\"/usr/sbin/ntpdate time.nist.gov &> /dev/null\"" }, "name": "run_cmd"},
            {"action": {"module": "shell", "args": "ifconfig"}, "name": "run_whoami"},
        ]
        ret = runner.run(tasks, "all")
        print(ret.results_summary)
        print(ret.results_raw)

def TestCommandRunner():
        """
        执行单个命令，返回结果
        :return:
        """

        host_data = [
            {
                "hostname": "192.168.10.102",
                "ip": "192.168.10.102",
                "port": 22,
                "username": "root",
                "password": "123456",
            },
        ]
        inventory = BaseInventory(host_data)
        runner = CommandRunner(inventory)

        #该模块可以运行command，shell，raw，script，直接写入参数即可。
        res = runner.execute('df -h', 'all')
        #res = runner.execute("/root/sayhell.sh", 'all')
        #print(res.results_command)
        res_command = res.results_command
        print('------------')
        print(json.dumps(res_command))

        #print(res.results_raw)
        print('-------------')
        print(json.dumps(res.results_raw))
        #print(res.results_command['10.135.133.214']['stdout'])

if __name__ == "__main__":
    #TestAdHocRunner()
    TestCommandRunner()
```



```python
context.CLIARGS = ImmutableDict(tags={}, 
                                listtags=False, 
                                listtasks=False, 
                                listhosts=False, 
                                syntax=False, 
                                connection='ssh', 
                                module_path=None, 
                                forks=5, 
                                remote_user='oracle', 
                                private_key_file=None,  
                                ssh_common_args=None, 
                                ssh_extra_args=None, 
                                sftp_extra_args=None, 
                                scp_extra_args=None, 
                                become=True,
                                become_method='sudo', 
                                become_user='oracle', 
                                verbosity=True, 
                                check=False, 
                                start_at_task=None)
```



> 注意： 目前测试过程中 become_method 参数一定要设置，否则出现下列报错
>
> `The error was: AttributeError: 'NoneType' object has no attribute 'startswith'`