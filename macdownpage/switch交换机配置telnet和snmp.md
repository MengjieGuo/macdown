#配置交换机的telnet以及snmp-agent

> 本次连接的环境:
> 
>>一台H3C的S26XX系列的交换机；一根usb转rj45的线；一台windows10电脑。
>>网线是电脑用来下载超级终端的。u转串口的线在连接交换机的console口和电脑的usb接口后
>>可能还需驱动，最好买不需要驱动，或者送驱动光盘的线吧。windows要安装超级终端。
> 
> 下面开始连接配置。

##连接
>使用u转串口线，去连接交换机的console口和window的usb接口。
>

##确认windows的com号
>在电脑的`设备管理`里面，找到`端口`，查看下拉列表中com号，类似`com3`这样的。
>当然可能有多个，这里就选com3吧。

##打开超级终端
>在windows中打开超级终端，配置的步骤一般是：
>###1. 新建连接
>输入一个随意的名称例如`test`，然后选取一个你喜欢的图标。
>###2. 选择
>国家地区`中国（86）`，区号`011`，电话可以跳过，连接时使用`COM3`，这个COM3就是上一步中查看的那个com号。
>###3. 设置com的属性
> 
> 
> 
> |名称 			|选项	|
> |:-----------	|:------:|
> |每秒位数（b）：|选择9600吧，毕竟H3C手册上这么建议的。|
> |数据位（d）：	|选择8|
> |奇偶校验（p）：|选择无|
> |停止位（s）：	|选择1|
> |数据流控制（f）：|选择无|
>
>
> 
> 确定后就等一下，会自动连接到交换机，此时可能终端界面白的如一张纸，回车一下，会出现类似`<H3C>`这样的标识，以及提示信息。正常情况下再回车几次就进入命令提示符`<H3C>`此时就可以进入配置阶段。如果无法连接成功，可能是com口没有选择好、配置好，一个一个试一下。
> 

##在超级终端配置交换机参数
>
> ```
> 提示：设置完成后一定要保存设置，并重启交换机，不然断电后再通电，你所做的修改
> 	   就失效了，等于白做。建议先认真读一下官方网站的配置参考文档。提示符一定
>      要对，不然无法识别命令。输入？可以获得可以识别的一些命令。
> ```
> 
> ### 第一次通过console口登录交换机
> ### 1. 在vlan中配置交换机的ip
> 
> 要想通过telnet方式连接交换机，必须先给交换机一个ip，这个ip的指定是根据交换机这个局域网的网段来选择的。学过计算机网络的话会很快理解，ip地址分网络号和主机号，网络号就可以说是网段。要想知道你所在局域网网段很简单啊，比如公司内网，主机之间的ip号的前几个肯定一样，比如都是`192.168.1`，那么就可以给交换机指定一个`192.168.1.8`，只要这个ip没有主机绑定就行。
> 
> ```
> <H3C>system-view
> [H3C]interface Vlan-interface 1
> [H3C-Vlan-interface]ip address 192.168.1.8 255.255.255.0
> ```
> 
>### 2. 配置Telnet信息。
> 配置完成后就可以使用Telnet进行管理了，直接在windows的命令行输入类似`telnet 192.168.1.123` 这样的命令，这个ip是交换机的ip，需要手动设置
> 
> ```
> <H3C>system-view
> Enter system view, return to user view with Ctrl+Z.
> [H3C]user-interface vty 0
> [H3C-vty]idle-timeout 7
> [H3C-vty]set authentication password H3C
> 
> ```
>### 3. 保存设置
>
>`注意：一定要保存啊`
>
>```
>[H3C-vty]return
><H3C>save
>This will save the configuration in the EEPROM memory 
Are you sure?[Y/N]y 
Now saving current configuration to EEPROM memory 
Please wait for a while… 
Current configuration saved to EEPROM memory successfully
```
>
>### 4. 重启交换机
>
````
<H3C>reboot
 This will reboot switch. Continue? [Y/N]y 
%0.4526951 H3C CMD_REBOOT/5/REBOOT:Next boot will be flash_b
Switch is rebooted! 
>
>

##通过windows主机连接交换机配置开启snmp-agent
> 配置完交换机之后，没有问题的话就能够在主机上面通过telnet连接交换机了，有线无线连接都可以。windows，mac，linux都可以。注意要在一个局域网内啊。
> ### 1. snmp的版本
> snmp有多个版本，每一个交换机可以同时支持多个版本的snmp协议，有v1、v2和v3版本。
> 本次的交换机支持v1和v2版本。
> 
> ```
> 提示：可以通过交换机命令查看版本，启用相应的版本	
snmp-agent sys-info version { all | { v1 | v2c | v3 } * }
```
> ### 2.配置SNMP——Agent
> <H3C>system-view
> [H3C]snmp-agent sys-info version v1
> [H3C]snmp-agent community read public
> [H3C]snmp-agent community write private
> [H3C]snmp-agnet trap enable
> [H3C]snmp-agent target-host trap address udp-domain 1.1.1.2 params securityname public v1				# 这条命令可能执行不成功，问题不大，过。
> ### 3.从另一台配有小米open-falcon的主机中启动switch
> 
> ```
> 注意：下面的内容是关于小米监控系统的，通过open-falcon可以监控交换机的运行情况。
> 关于怎么配置open-falcon的switch模块，见《open-falcon安装配置》。
> ```
> 
> 配置完switch的配置文件，通过sudo ./control start命令就可以从dashboard模块看到交换机各个端口的信息了。
> 
>
