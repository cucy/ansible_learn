#!/usr/bin/env python
# _*_ coding:utf8 _*_ 

# 核心class
from collections import namedtuple

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
variable_manager = VariableManager(loader=loader, inventory=inventory)
"""
loader 传入loader对象,读取yaml资源配置文件
inventory 
"""


# Options 类
Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])

options = Options(connection='smart', module_path=None, forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)

# Play 执行对象和模块
play_soure =dict(
        name = "Ansible Play ad-host test",
        hosts = ['192.168.193.140','192.168.193.139'],
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='command', args='pwd'), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
         ]
    )


play = Play().load(data=play_soure, variable_manager=variable_manager, loader=loader)

passwords=dict()

tqm = TaskQueueManager (
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader, 
    options=options,
    passwords=passwords, stdout_callback=None, run_additional_callbacks=True, run_tree=False

)
result = tqm.run(play=play)


"""
$ python ansible_api_k1.py

PLAY [Ansible Play ad-host test] **********************************************************************************************************************************************************************************************

TASK [command] ****************************************************************************************************************************************************************************************************************
changed: [192.168.193.140]
changed: [192.168.193.139]

TASK [debug] ******************************************************************************************************************************************************************************************************************
ok: [192.168.193.140] => {
    "msg": "/Users/zrd/PycharmProjects/ansible_learn/script"
}
ok: [192.168.193.139] => {
    "msg": "/Users/zrd/PycharmProjects/ansible_learn/script"
}

"""
