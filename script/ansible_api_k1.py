#!/usr/bin/env python
# _*_ coding:utf8 _*_ 

# 核心class

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


# InventoryManager
""" 管理主机，主机组相关资源信息 """


# 读取yaml文件信息
loader = DataLoader()

inventory= InventoryManager(loader=loader,sources=["my_hosts"])
"""
loader 怎样的方式读取配置文件
sources 列表形式读取信息， 相对路径，绝对路径    l
"""



# VariableManager 类
VariableManager(loader=loader, inventory=inventory)
"""
loader 传入loader对象,读取yaml资源配置文件
inventory 
"""
