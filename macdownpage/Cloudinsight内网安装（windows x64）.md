#在内网环境中，给windows（x64）安装Cloudinsight

`这里是将windows作为内网主机，如果需要将windows作为联网`
## 1、环境前提
> ```
> 前提是已经了有一个安装了Cloudinsight的主机A，主机A能够与外网通讯。
> 这台内网windows主机就可以通过主机A传递数据。
> 理解Cloudinsight的运行方式。
> ```

## 2、到Cloudinsight上面登陆你的账号
> [点击oneapm登陆](https://cloud.oneapm.com)

## 3、下载安装文件到本地
> ```
> 1.左侧是我们的菜单栏，选择平台，会出现‘平台’和‘拓扑’选项。
> 2.选择‘平台’，因为选‘拓扑’看不到‘添加平台按钮’。
> 3.选择右上角`添加平台`按钮。
> 4.从中选择自己想安装的平台，这里想安装在windows上面。根据电脑的位数选择‘32’或‘64’进行下载。注意复制licensekey。
> ```

## 4、传送文件到windows主机
>```
> 把下载的安装文件和licensekey文件（把licensekey写入文件）传给windows，可以使用U盘，ftp，只要能传文件。
> ```

## 5、windows安装cloudinsight
> ```
> 1、通过双击msi文件安装。点击我们的刚刚传递过来的文件进行安装，如果计算机允许当前安装操作，在选择完安装目录之后就可以正常安装完成。
> 2.通过命令行安装。cd到cloudinsight目录。
> msiexec /qn /i cloudinsight-agent.msi 
> 32位
> CI_LICENSE_KEY="AQEFBVcOA1E7062MTRwSThNJSVc81alFWl5PCgFQD8a680wGD0kJV0kFd9ceAQcFTggHTAlR"
> 64位
> msiexec /qn /i cloudinsight-agent.amd64.msi CI_LICENSE_KEY="AQEFBVcOA1E7062MTRwSThNJSVc81alFWl5PCgFQD8a680wGD0kJV0kFd9ceAQcFTggHTAlR"
> 
> ```
## 6、测试是否能够连通主机A
>```
> 如果无法连通，在oneapm网页上面看到windows主机的数据，因为windows主机使用主机A转发数据。
> 如何测试？？？待会再解决
> ```
## 7、配置文件
> 
> 
> ```
> 下面的操作都是在windwos上面
> 1.若果可以操作桌面，点击‘开始’，‘所有程序‘里面会多一个cloudinsight选项，点击里面的启动文件，会出现cloudinsight程序的界面。左侧是配置文件和启动停止操作菜单。
> 2.选择‘Settings’按钮，就会进入平台的配置文件。
> ```
> 需要的配置
> 
> ```
> # 要把数据发送给哪一台主机，这里是主机A，前提是主机A配置了non_local_traffic:yes。
> ci_url: http://192.168.1.2:100010 
> 
> # 你的独有license_key，这个license_key就是前面拿到的那个，可以在oneapm得到，下面是我的key。
> license_key: CI_LICENSE_KEY=AQEFBVcOA1E7062MTRwSThNJSVc81alFWl5PCgFQD8a680wGD0kJV0kFd9ceAQcFTggHTAlR
> 
>  # 你的主机名，为了在oneapm中区分每一台主机，起个名字，类似windows.sever.220。
> hostname : windows.server.112
> 
> # 标签，可以随意取，当然又要意义，需要的时候再写也可以，标签可以有多个。
> # tags: windows-tag-112
> # 配置生成日志的级别，waring，info之类的，可以不要，注释了。
> # log_level: INFO
> # ？？？
> # log_to_event_viewer: no
> ```
>