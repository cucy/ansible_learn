###1.1. 用于读取yaml，json格式的文件 from ansible.parsing.dataloader import DataLoader

###1.2. 用于管理变量的类，包括主机，组，扩展等变量 from ansible.vars.manager import VariableManager

###1.3. 用于创建和管理inventory，导入inventory文件 from ansible.inventory.manager import InventoryManager

###1.4. 存储着角色列表，任务，处理代码块 from ansible.playbook.play import Play

###1.5. ad-hoc ansible底层用到的任务队列 from ansible.executor.task_queue_manager import TaskQueueManager

###1.6. 回调基类，用来定义回调事件，比如返回失败成功等信息 from ansible.plugins.callback import CallbackBase

###1.7. 执行playbook from ansible.executor.playbook_executor import PlaybookExecutor

###1.8. 操作单个主机 from ansible.inventory import host

###1.9. 操作单个主机组 from ansible.inventory import group





# InventoryManager模块说明

```
# 实例化需要两个参数
# 参数一为读取yml文件的信息，需要实例化 DataLoader
# 参数二为读取从那个位置读取资产配置文件，多个可逗号分割
intertory = InventoryManager(loader='',sources='')

# 以字典的方式打印出主机和主机组相关信息
intertory.get_group_dict()

# 获取所有的主机
inventory.get_hosts()

# 添加主机到指定主机组
# 参数一指定主机地址
# 参数二指定主机端口
# 参数三指定主机群组，必须存在的群组
inventory.add_host(host='1.1.1.1',port=2222,group='web_server')

# 获取指定的主机对象
inventory.get_host(hostname='1.1.1.1')
```



# VariableManager模块说明

```
# 实例化需要两个参数
# 参数一为读取yml文件的信息，需要实例化 DataLoader
# 参数二为资产管理配置变量
variable = VariableManager(loader=loader,inventory=inventory)

# 获取变量
variable.get_vars()

# 查看指定主机的详细变量信息
# 传入的host是inventory.get_host获得的主机对象
host = inventory.get_host(hostname='1.1.1.1')
host_vars = variable.get_vars(host=host)

# 设置主机变量方法 
# 传入的host是inventory.get_host获得的主机对象
host = inventory.get_host(hostname='1.1.1.1')
variable.set_host_variable(host=host,varname='ansible_ssh_pass',value='12345')

# 添加扩展变量
# 参数是一个字典多个逗号分割
variable.extra_vars={'devops':'best'}
```




``` 
In [1]: from ansible.parsing.dataloader import DataLoader

In [2]: from ansible.inventory.manager import InventoryManager

In [3]: loader = DataLoader()

In [4]: inventory= InventoryManager(loader=loader,sources=["my_hosts"])


In [5]: inventory.
 add_group()           get_vars()            parse_sources()
 add_host()            groups                reconcile_inventory()
 clear_caches()        hosts                 refresh_inventory()
 clear_pattern_cache() list_groups()         remove_restriction()
 get_groups_dict()     list_hosts()          restrict_to_hosts()
 get_host()            localhost             subset()
 get_hosts()           parse_source()


# 获取组名
In [6]: inventory.get_groups_dict()
Out[6]:
{'all': ['192.168.193.139', '192.168.193.140'],
 'test_group0': ['192.168.193.139', '192.168.193.140'],
 'test_group1': ['192.168.193.139', '192.168.193.140'],
 'test_group2': ['192.168.193.139', '192.168.193.140'],
 'ungrouped': []}
 
 
# 获取所有主机列表
In [12]: inventory.get_hosts()
Out[12]: [192.168.193.139, 192.168.193.140, 192.168.193.143]


# 添加主机

In [13]: inventory.add_host(host="192.168.1.33",port=22, group="test_group1")

In [14]: inventory.get_groups_dict()
Out[14]:
{'all': ['192.168.193.139',
  '192.168.193.140',
  '192.168.193.143',
  '192.168.1.33'],
 'test_group0': ['192.168.193.139',
  '192.168.193.140',
  '192.168.193.143',
  '192.168.1.33'],
 'test_group1': ['192.168.193.139',
  '192.168.193.140',
  '192.168.193.143',
  '192.168.1.33'],
 'test_group2': ['192.168.193.139', '192.168.193.140'],
 'ungrouped': []}
 
In [16]: inventory.get_host(hostname="192.168.1.33")
Out[16]: 192.168.1.33
```
