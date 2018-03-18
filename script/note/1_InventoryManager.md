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
