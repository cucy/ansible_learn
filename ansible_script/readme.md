


```shell

ansible-playbook basic-service.yml -i environments/prod -u sysops --become --key-file=files/ssh-key/ssh-key -t install_mysql



ansible-playbook basic-service.yml -i environments/prod   -t install_mysql
```


#  安装MySQL


`修改host文件`

``` 
ansible-playbook basic-service.yml -i environments/prod  --limit mysql_host    -t install_mysql 

```
