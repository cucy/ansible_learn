#!/usr/bin/env python
# _*_ coding:utf8 _*_ 

# 核心class
from collections import namedtuple

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.playbook import *
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

# InventoryManager
""" 管理主机，主机组相关资源信息 """

# 读取yaml文件信息
loader = DataLoader()

inventory = InventoryManager(loader=loader, sources=["my_hosts"])
"""
loader 怎样的方式读取配置文件
sources 列表形式读取信息， 相对路径，绝对路径    l
"""

# VariableManager 类
variable_manager = VariableManager(loader=loader, inventory=inventory)
"""
loader 传入loader对象,读取yaml资源配置文件
inventory 
"""

# Options 类
Options = namedtuple('Options',
                     ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff',
                      "listhosts","listtasks","listtags", "syntax"])

options = Options(connection='smart', module_path=None, forks=10, become=None, become_method=None, become_user=None,
                  check=False, diff=False, listhosts=None,listtasks=None,listtags=None, syntax=None)

#  PlaybookExecutor 类

passwords = dict()

play_book = PlaybookExecutor(
    playbooks=["fbook1.yaml"],

    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    options=options,
    passwords=passwords
)

play_book.run()



"""
$ python ansible_api_k2.py

PLAY [192.168.193.139,192.168.193.140] ****************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************
fatal: [192.168.193.139]: FAILED! => {"msg": "to use the 'ssh' connection type with passwords, you must install the sshpass program"}
ok: [192.168.193.140]

TASK [touch file] *************************************************************************************************************************************************************************************************************
 [WARNING]: Consider using file module with state=touch rather than running touch

"""
