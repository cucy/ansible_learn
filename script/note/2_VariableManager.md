``` 
In [1]: from ansible.parsing.dataloader import DataLoader
   ...: from ansible.vars.manager import VariableManager
   ...: from ansible.inventory.manager import InventoryManager
   
  
In [2]: loader = DataLoader()
   ...:
   ...: inventory= InventoryManager(loader=loader,sources=["my_hosts"])
  
  
In [3]: variable_manger=VariableManager(loader=loader, inventory=inventory)

In [4]: variable_manger.
                         clear_facts()             get_vars()                set_host_facts()          set_inventory()
                         extra_vars                options_vars              set_host_variable()       set_nonpersistent_facts()


In [4]: variable_manger.get_vars()
Out[4]:
{'ansible_playbook_python': '/Users/zrd/.pyenv/versions/3.5.3/envs/sx3.5.3/bin/python',
 'groups': {'all': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group0': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group1': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group2': ['192.168.193.139', '192.168.193.140'],
  'ungrouped': []},
 'omit': '__omit_place_holder__aa69d3135041aca8d91a53da1e1e2ece7b2c7357',
 'playbook_dir': '/Users/zrd/PycharmProjects/ansible_learn/script'}
 


# 获取变量信息
In [5]: host = inventory.get_host(hostname="192.168.193.139")
In [6]: variable_manger.get_vars(host=host)
Out[6]:
{'ansible_playbook_python': '/Users/zrd/.pyenv/versions/3.5.3/envs/sx3.5.3/bin/python',
 'ansible_ssh_pass': 'changan',
 'ansible_ssh_user': 'root',
 'group_names': ['test_group0', 'test_group1', 'test_group2'],
 'groups': {'all': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group0': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group1': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group2': ['192.168.193.139', '192.168.193.140'],
  'ungrouped': []},
 'inventory_dir': '/Users/zrd/PycharmProjects/ansible_learn/script',
 'inventory_file': '/Users/zrd/PycharmProjects/ansible_learn/script/my_hosts',
 'inventory_hostname': '192.168.193.139',
 'inventory_hostname_short': '192',
 'omit': '__omit_place_holder__aa69d3135041aca8d91a53da1e1e2ece7b2c7357',
 'playbook_dir': '/Users/zrd/PycharmProjects/ansible_learn/script'}
 
# 设置变量信息
""" host传入host对象，varname修改配置名， value设置值 """

In [7]: variable_manger.set_host_variable(host=host, varname="ansible_ssh_pass", value="123456")
In [8]: variable_manger.get_vars(host=host)
Out[8]:
{'ansible_playbook_python': '/Users/zrd/.pyenv/versions/3.5.3/envs/sx3.5.3/bin/python',
 'ansible_ssh_pass': '123456',
 'ansible_ssh_user': 'root',
 'group_names': ['test_group0', 'test_group1', 'test_group2'],
 'groups': {'all': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group0': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group1': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group2': ['192.168.193.139', '192.168.193.140'],
  'ungrouped': []},
 'inventory_dir': '/Users/zrd/PycharmProjects/ansible_learn/script',
 'inventory_file': '/Users/zrd/PycharmProjects/ansible_learn/script/my_hosts',
 'inventory_hostname': '192.168.193.139',
 'inventory_hostname_short': '192',
 'omit': '__omit_place_holder__aa69d3135041aca8d91a53da1e1e2ece7b2c7357',
 'playbook_dir': '/Users/zrd/PycharmProjects/ansible_learn/script'}
 

# 扩展变量
In [9]: variable_manger.extra_vars={"my_web": "github.com", "name":"zrd"}
In [10]: variable_manger.get_vars(host=host)
Out[10]:
{'ansible_playbook_python': '/Users/zrd/.pyenv/versions/3.5.3/envs/sx3.5.3/bin/python',
 'ansible_ssh_pass': '123456',
 'ansible_ssh_user': 'root',
 'group_names': ['test_group0', 'test_group1', 'test_group2'],
 'groups': {'all': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group0': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group1': ['192.168.193.139', '192.168.193.140', '192.168.193.143'],
  'test_group2': ['192.168.193.139', '192.168.193.140'],
  'ungrouped': []},
 'inventory_dir': '/Users/zrd/PycharmProjects/ansible_learn/script',
 'inventory_file': '/Users/zrd/PycharmProjects/ansible_learn/script/my_hosts',
 'inventory_hostname': '192.168.193.139',
 'inventory_hostname_short': '192',
 'my_web': 'github.com',
 'name': 'zrd',
 'omit': '__omit_place_holder__aa69d3135041aca8d91a53da1e1e2ece7b2c7357',
 'playbook_dir': '/Users/zrd/PycharmProjects/ansible_learn/script'}
```
