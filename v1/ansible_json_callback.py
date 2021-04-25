# 核心类
import json
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

###############################
# VariableManager 类
###############################
variable_manager = VariableManager(loader=loader, inventory=inventory_manager)

# 方法2
context.CLIARGS = ImmutableDict(
    connection='smart', module_path=None, verbosity=5,
    forks=10, become=None, become_method=None,
    become_user=None, check=False, diff=False,
    syntax=None, start_at_task=None,
    gather_facts='no',
)
passwords = dict()

play_book = PlaybookExecutor(playbooks=['testplaybook.yml'],
                             inventory=inventory_manager,
                             variable_manager=variable_manager,
                             loader=loader,
                             passwords=passwords

                             )


# Create a callback plugin so we can capture the output
class ResultsCollectorJSONCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in.

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin.
    """

    def __init__(self, *args, **kwargs):
        super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        self.host_ok[host.get_name()] = result
        # print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result


results_callback = ResultsCollectorJSONCallback()
play_book._tqm._stdout_callback = results_callback

play_book.run()

print("UP ***********")
for host, result in results_callback.host_ok.items():
    print('{0} >>> {1}'.format(host, result._result))

print("FAILED *******")
for host, result in results_callback.host_failed.items():
    print('{0} >>> {1}'.format(host, result._result['msg']))

print("DOWN *********")
for host, result in results_callback.host_unreachable.items():
    print('{0} >>> {1}'.format(host, result._result['msg']))
