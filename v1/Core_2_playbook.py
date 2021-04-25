# 核心类
from collections import namedtuple
from optparse import Values

from ansible.parsing.dataloader import DataLoader
from ansible.playbook import Playbook
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

from ansible import context
from ansible.module_utils.common.collections import ImmutableDict

###############################
# InventoryManager 类
###############################
# 读取资产清单信息
loader = DataLoader()

"""
sources 可以是绝对和相对路径
"""

inventory_manager = InventoryManager(loader=loader, sources=['my_hots.txt'])

###############################
# VariableManager 类
###############################
variable_manager = VariableManager(loader=loader, inventory=inventory_manager)

# 方法2
context.CLIARGS = ImmutableDict(
    connection='smart', module_path=None, verbosity=5,
    forks=10, become=None, become_method=None,
    become_user=None, check=False, diff=False,
    syntax=None, start_at_task=None
)
passwords = dict()

play_book = PlaybookExecutor(playbooks=['testplaybook.yml'],
                             inventory=inventory_manager,
                             variable_manager=variable_manager,
                             loader=loader,
                             passwords=passwords,

                             )

play_book.run()
