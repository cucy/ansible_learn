# 核心类
from collections import namedtuple
from optparse import Values

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

from ansible import context
from ansible.module_utils.common.collections import ImmutableDict


# print(__file__)

###############################
# InventoryManager 类
###############################
# 读取资产清单信息
loader = DataLoader()

"""
sources 可以是绝对和相对路径
"""

inventory_manager = InventoryManager(loader=loader, sources=['my_hots.txt'])
print(inventory_manager.list_hosts())
print(inventory_manager.list_groups())
print(inventory_manager.get_groups_dict() )
print(inventory_manager.get_groups_dict()['all'])

"""
[192.168.1.80, 192.168.1.76, 192.168.1.77]
['all', 'test_group1', 'ungrouped']
{'all': ['192.168.1.80', '192.168.1.76', '192.168.1.77'], 'ungrouped': [], 'test_group1': ['192.168.1.80', '192.168.1.76', '192.168.1.77']}
"""

print(inventory_manager.get_hosts())
"""
[192.168.1.80, 192.168.1.76, 192.168.1.77]
"""

# 添加主机
inventory_manager.add_host(host='192.168.1.1', port=12, group='test_group1')

print(inventory_manager.list_hosts())

###############################
# VariableManager 类
###############################
variable_manager = VariableManager(loader=loader, inventory=inventory_manager)

print(variable_manager.get_vars())
'''
{
    "playbook_dir":"/tmp/pycharm_project_59",
    "ansible_playbook_python":"/usr/bin/python3",
    "groups":{
        "all":[
            "192.168.1.80",
            "192.168.1.76",
            "192.168.1.77",
            "192.168.1.1"
        ],
        "ungrouped":[

        ],
        "test_group1":[
            "192.168.1.80",
            "192.168.1.76",
            "192.168.1.77",
            "192.168.1.1"
        ]
    },
    "omit":"__omit_place_holder__087a4fa8ed57a0659c5e5f3a1adee4445814c5b0",
    "ansible_version":"Unknown"
}
'''

# 添加, 修改 扩展变量
host = inventory_manager.get_host(hostname='192.168.1.76')
print(variable_manager.get_vars(host=host))
"""
{
    "inventory_file":"/tmp/pycharm_project_59/my_hots.txt",
    "inventory_dir":"/tmp/pycharm_project_59",
    "inventory_hostname":"192.168.1.76",
    "inventory_hostname_short":"192",
    "group_names":[
        "test_group1"
    ],
    "ansible_facts":{

    },
    "playbook_dir":"/tmp/pycharm_project_59",
    "ansible_playbook_python":"/usr/bin/python3",
    "groups":{
        "all":[
            "192.168.1.80",
            "192.168.1.76",
            "192.168.1.77",
            "192.168.1.1"
        ],
        "ungrouped":[

        ],
        "test_group1":[
            "192.168.1.80",
            "192.168.1.76",
            "192.168.1.77",
            "192.168.1.1"
        ]
    },
    "omit":"__omit_place_holder__3909aaf2b72b39148f1cf8db39bfdb4745bec16d",
    "ansible_version":"Unknown"
}
"""
variable_manager.set_host_variable(host=host, varname='ansible_ssh_pass', value='dsfnbhjkdasnfjkdsaf')
print(variable_manager.get_vars(host=host))

# variable_manager.extra_vars


Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                 'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                                 'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                 'verbosity',
                                 'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])

# 方法1
# ops = Values(Options)
# context._init_global_context(ops)

# 方法2
context.CLIARGS = ImmutableDict(
      connection='smart', module_path=None, verbosity=5,
      forks=10, become=None, become_method=None,
      become_user=None, check=False, diff=False)
 
# Play  执行对象和模块
play_soure = dict(
    name="Ansible Play ad-hoc",
    hosts=[str(h) for h  in inventory_manager.list_hosts()],
    gather_facts=False,
    tasks=[
        dict(action='shell touch  "/tmp/12312344123412341.txt" '),
        dict(action=dict(module='shell', args='ls -l  /tmp'), register='shell_out'),
        dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}'))),
        dict(action=dict(module='command', args=dict(cmd='/usr/bin/uptime'))),
    ],

)

play = Play().load(play_soure, variable_manager=variable_manager, loader=loader,)

passwords = dict()
tqm = TaskQueueManager(inventory=inventory_manager,
                       variable_manager=variable_manager,
                       loader=loader,
                       passwords=passwords,
                       # options=options,
                       
                       )

tqm.run(play)
tqm.cleanup()

