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
                     ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])

options = Options(connection='smart', module_path=None, forks=10, become=None, become_method=None, become_user=None,
                  check=False, diff=False)

# Play 执行对象和模块
play_soure = dict(
    name="Ansible Play ad-host test",
    hosts=['192.168.193.140', '192.168.193.139'],
    gather_facts='no',
    tasks=[
        dict(action=dict(module='command', args='/usr/bin/touch /tmp/test.log'), ),  # register='shell_out'),
        # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
    ]
)

play = Play().load(data=play_soure, variable_manager=variable_manager, loader=loader)


# CallbackBase 类
class ModelResultCollector(CallbackBase):
    """
      rewirte CallbackBase class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.host_failed[result._host.get_name()] = result


callback = ModelResultCollector()

passwords = dict()

tqm = TaskQueueManager(
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    options=options,
    passwords=passwords,
    # stdout_callback=None,
    stdout_callback=callback,
    run_additional_callbacks=True,
    run_tree=False

)
result = tqm.run(play=play)

#  打印taskresult输出
print(callback.host_ok.items())
print(callback.host_failed.items())
print(callback.host_unreachable.items())

result_raw = {
    "sucess": {},
    "failed": {},
    "unreachable": {}}

for host, result in callback.host_ok.items():
    result_raw["sucess"][host] = result._result

for host, result in callback.host_failed.items():
    result_raw["failed"][host] = result._result

for host, result in callback.host_unreachable.items():
    result_raw["unreachable"][host] = result._result

print(result_raw)

"""
$ python ansible_api_k3_callback.py 
dict_items([('192.168.193.140', <ansible.executor.task_result.TaskResult object at 0x10ff27f60>)])
dict_items([('192.168.193.139', <ansible.executor.task_result.TaskResult object at 0x10ff25ef0>)])
dict_items([])
{'sucess': {'192.168.193.140': {'start': '2018-03-18 05:10:58.798907', 'warnings': ['Consider using file module with state=touch rather than running touch'], 'changed': True, 'delta': '0:00:00.001974', 'end': '2018-03-18 05:10:58.800881', '_ansible_parsed': True, 'stdout': '', 'invocation': {'module_args': {'chdir': None, 'stdin': None, '_raw_params': '/usr/bin/touch /tmp/test.log', 'warn': True, 'executable': None, 'creates': None, 'removes': None, '_uses_shell': False}}, 'stdout_lines': [], 'stderr_lines': [], 'stderr': '', 'cmd': ['/usr/bin/touch', '/tmp/test.log'], '_ansible_no_log': False, 'rc': 0}}, 'unreachable': {}, 'failed': {'192.168.193.139': {'msg': "to use the 'ssh' connection type with passwords, you must install the sshpass program"}}}

"""
