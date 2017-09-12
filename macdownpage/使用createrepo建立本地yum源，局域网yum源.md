# 使用createrepo建立本地yum源，局域网yum源
```为什么要建立本地yum源和局域网yum源？因为服务器是不能暴露在互联网上面的，当需要向服务器安装软件时就需要实现下载好所有的依赖。
对于多台服务器都需要一份依赖就会显得麻烦，不如	让其中一台服务器当作yum源，其他的服务器只需要到这台服务器找依赖就OK了。
```

# 本地yum源
## 下载本地yum源制作工具
1. 建立本地yun源需要一个工具，*createrepo*。
2. 下载*createrepo*。

> $ yum install -y yum-plugin-downloadonly createrepo

联网的情况下可以直接安装，如果不能访问网络，可以让能访问网络的主机下载好安装包，scp到服务器。（暂时没有尝试）

## 制作yum源
1. 需要把一个目录当作一个存放依赖包的仓库。
> $ mkdir /home/yum_local_resource

2. 把这个目录作为yum源仓库
> createrepo /home/yum_local_resource

3. copy rpm包到这个目录下，可以对rpm再进行区分，把不同软件的rpm包依赖放到/home/yum_local_resource/的不同目录下。这里把docker和依赖所在的目录copy到/home/yum_local_resource/
> cp -r /home/docker_repo/ /home/yum_local_resource

4. 清理yum缓存??
> $ yum clean all
> 
> $ yum makecache

5. 每当我们添加了一些rpm包到/home/yum_local_resource/时需要
> $ createrepo --update /home/yum_local_resource

## 让yum命令指向本地寻找软件包
	其实yum还有另一个命令 yum localinstall ，就是在当前目录安装寻找rpm包，
	但是由于遇到了明明已经下载了，但是还是提示找不到rpm包的情况。
	所以决定构建本地yum源。
	yum源的配置文件在/etc/yum.repo.d/，为了维护方便，直接备份一份，然后把下面的文件全删除。
	再新建一个文件CentOS-Local.repo配置文件。
	
> $ cp -r /etc/yum.repo.d/ /etc/yum.repo.d.back/
> 
> $ cd /etc/yum.repo.d/
> 
> $ rm -f *
> 
> $ touch CentOS-Local.repo
> 
> $ vi CentOS-Local.repo

添加内容

```
[local]
name=Local Yum
baseurl=file:///home/yum_local_resource
gpgcheck=0
enabled=1
```

保存退出
正常的话，通过yum localinstall docker-1.10.1.rpm 就可以用 yum install docker 代替。
怎么获取docker的依赖？？？使用命令
> $ repotrack docker

会把docker以及它的依赖下载到当前目录，所以最好建立一个空目录再使用这个命令。

# 建立局域网yum源

