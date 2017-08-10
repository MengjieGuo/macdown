#内网环境给CentOS安装Cloudinsight
>```
>如果联网的话安装比较简单，可以直接使用官方提供的安装命令。
CI_LICENSE_KEY=AQEFBVcOA1E7062MTRwSThNJSVc81alFWl5PCgFQD8a680wGD0kJV0kFd9ceAQcFTggHTAlR 
bash -c "$(curl -L https://download.oneapm.com/oneapm_ci_agent/install_agent.sh)"
```

## 1、下载rpm安装包
>[下载网址](http://yum.oneapm.com/x86_64/)
>
>```
在这个目录下有多个版本，随便选一个吧。
这里选择
cloudinsight-agent_4.7.2-1.x86_64.rpm
可以命令行下载
wget http://yum.oneapm.com/x86_64/cloudinsight-agent-4.7.2-1.x86_64.rpm
```

## 2、把rpm包传给要安装Cloudinsight的CentOS主机A
> 使用ftp的话，可以使用命令行，或者下载一个工具，比如`Cyberduck`


## 3、安装Cloudinsight
>使用命令
`rpm -Uvh cloudinsight-agent-x.x.0-1.x86_64.rpm`
没有错误提示信息的话就安装成功了
`注意，此时联网的主机不能开启代理服务`

## 4、配置文件
>
> 配置文件在`/etc/cloudinsight-agent/`，这个目录下有平台和服务的配置文件。
> 平台的的配置文件是 `cloudinsight-agent.conf`
> 服务的配置文件在 `conf.d/`，下面有很多配置文件，需要是可以cp一份出来。
> 
> 安装目录在`/etc/init.d/`，通过它可以start | restart | stop | status | info等命令，形式是 `/etc/init.d/cloudinsight-agent start`。
> 
> 需要的配置
> 
> ```
> # 数据将发送到的主机，不像小米的open-falcon，这里必须把数据发给他们。如果不喜欢发给他们，可以部署open-falcon。
> ci_url: https://dc-cloud.oneapm.com
> 
> # 你的独有license_key
> license_key: AQEFBVcOA1E7062MTRwSThNJSVc81alFWl5PCgFQD8a680wGD0kJV0kFd9ceAQcFTggHTAlR
> 
> # 自己给主机起个名字，标识主机
> hostnaem: centos.server.
> 
> # 标签，可以有多个，需要时配置
> # tags:tag1, env:env1
> 
> # 监听的端口
> listen_port: 10010
> 
> # 如果你想让主机作为内网中负责通讯的主机，否则就，no
> non_local_traffic: true
> 
> # 日志
> log_level: INFO
> log_to_syslog: yes
> ```

# 5、重启服务
> 重启`/etc/cloudinsight-agent/restart`
> 
> 没有错误的话就可以到浏览器上面看到主机和数据了。