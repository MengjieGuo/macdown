# Devicemapper: Can't set cookie dm_task_set_cookie failed

在不断的docker-compose stop up过程中，信号量可能没有正确的释放。

[参考](https://github.com/kubevirt/kubevirt/issues/321)

运行命令
> `$ echo 'y' | sudo dmsetup udevcomplete_all`

也可以先

> '$ sudo dmsetup udevcomplete_all'

当询问时再yes