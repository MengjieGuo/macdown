# docker-compose启动问题can't set cookie dm_task_set_cookie failed
在项目更增加新功能或着修改功能时，需要用启动新的docker `container`，关闭旧的`container`。此时会遇到信号量没有被释放的问题，那么为什么会产出这个问题？能否避免这个问题？怎么释放已有的信号量？释放信号量对程序有什么影响？

## 问题
```
devmapper: Error activating devmapper device for 
'a3a8ef15dacd40ab6763fa98109dada3b5fbe955dc788c5136b4afba4736c552-init': 
Devicemapper: Can't set cookie dm_task_set_cookie failed

```
## 搜索后，参考[can't set cookie dm_task_set_cookie failed](https://github.com/kubevirt/kubevirt/issues/321)提出的解决方案

```
Thanks for reporting this! Are you using our Vagrant setup, or do you run your own infrastructure? 
We have seen this in our CentOS based Vagrant setup (#241), but it should be fixed in CentOS already.

Running

echo 'y' | sudo dmsetup udevcomplete_all
on affected nodes should be sufficient, instead of restarting docker.

```

> 提供的方案是运行下面的命令

`$ echo 'y' | sudo dmsetup udevcomplete_all`

> 这条命令实际上是为了释放系统的信号量，并输入`y`同意操作。
`dmsetup udevcomplete_all`命令的作用参考[dmsetup udevcomplete_all](https://access.redhat.com/documentation/zh-CN/Red_Hat_Enterprise_Linux/7/html/Logical_Volume_Manager_Administration/udev_device_manager.html)

|命令	|描述
|:---|:---:|
|dmsetup udevcomplete	|用于通知 udev 已经完成规则处理并解锁等待的进程（从 95-dm-notify.rules 的 udev 规则调用）。
dmsetup udevcomplete_all	|用于在调整过程中手动解锁所有等待进程。
dmsetup udevcookies	|用于在 debug 过程中显示所有现有 cookies（系统范围的信号）。
dmsetup udevcreatecookie	|用于手动创建 cookie（信号）。这在同一同步资源中运行多个进程时有用。
dmsetup udevreleasecookie	|ß用于等待所有与同步 cookie 中的所有进程关联的 udev 进程。



