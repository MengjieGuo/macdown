# centos7开启80端口，selinux ， iptables， firewalld
```
因为刚刚装机好centos7服务器，一切都是初始化状态，所以很多端口都是不开放的，
使用ip+port访问时都会出现connection oef的信息，所以需要先开启80端口
```

## iptables和firewalld
- iptables和firewalld都是防火墙工具，firewalld更加的高级，好用。
- 参照网上的iptables教程，大部分都是在添加完端口后重启服务，像这样
[iptables](http://www.cnblogs.com/kreo/p/4368811.html)但是本人遇到了这样的问题

```
$ service iptables save
The service command supports only basic LSB actions (start, stop, restart, try-restart, reload,
 force-reload, status). For other actions, please try to use systemctl.
 
好像是没有注册为服务之类的？？
```

```
iptables -L -n #查看iptables现有规则
iptables -P INPUT ACCEPT #先允许所有,不然有可能会杯具
iptables -F #清空所有默认规则
iptables -X #清空所有自定义规则
iptables -Z #所有计数器归0
iptables -A INPUT -i lo -j ACCEPT #允许来自于lo接口的数据包(本地访问)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT #开放22端口
iptables -A INPUT -p tcp --dport 21 -j ACCEPT #开放21端口(FTP)
iptables -A INPUT -p tcp --dport 80 -j ACCEPT #开放21端口(FTP)
iptables -A INPUT -p tcp --dport 443 -j ACCEPT #开放443端口(HTTPS)
iptables -A INPUT -p icmp --icmp-type 8 -j ACCEPT #允许ping
iptables -A INPUT -m state --state  RELATED,ESTABLISHED -j ACCEPT #允许接受本机请求之后的返回数据 RELATED,是为FTP设置的
iptables -P INPUT DROP #其他入站一律丢弃
iptables -P OUTPUT ACCEPT #所有出站一律绿灯
iptables -P FORWARD DROP #所有转发一律丢弃
service iptables save #保存上述规则
#注册iptables服务
#相当于以前的chkconfig iptables on
systemctl enable iptables.service
#开启服务
systemctl start iptables.service
#查看状态
systemctl status iptables.service
```
更加好用的工具还是firewalld，有的centos在装机时就已经安装了firewalld，如果没有安装，可以另外安装。
[]()

### 开启80端口 --permanent是永久开启的意思 --zone

`$ firewall-cmd --zone=public --add-port=80/tcp --permanent`
重启firewalld服务
systemctl restart firewalld.service

connection refused，说明端口开启了但是被防火墙阻止了

centos7还有selinux安全机制，关闭selinux

iptables -L -n

sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
setsebool -P httpd_can_network_connect 1

source /etc/selinux/config


nginx -t 
nginx 
# 测试网站连通
curl --proxy 192.168.1.128 http://www.baidu.com 
curl --proxy 192.168.1.128 http://www.nginx.org