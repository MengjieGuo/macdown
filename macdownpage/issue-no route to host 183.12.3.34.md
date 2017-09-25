# issue-no route to host 183.12.3.34
docker容器要使用本机的redis的6379端口，提示no route to host

docker的运行环境

所以需要防火墙开启端口6379

> 查询6379端口是否打开

`firewall-cmd --permanent --query-port=6379/tcp`

> 查看防火墙过滤规则

`iptables -L -n`

> 添加6379端口

`firewall-cmd --zone=public --permanent --add-port=6379/tcp`