
# centos服务器iptable端口禁用和selinux导致的pemmition denined

## 关闭selinux
`$ sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config`

## 开启selinux
`$ setsebool -P httpd_can_network_connect 1`