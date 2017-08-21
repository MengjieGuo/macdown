# 制作Docker镜像，编写docker-compose.yml
## 怎么制作wx_fine、auto_fetch的镜像
### 1 项目需要的镜像
|   仓库repository   |	版本tag   |		 
|:--|:-----:|
|	rabbitmq	| 3-management	|
|	postgres	| 9.6				|
|  	python		| 3					|
|	nginx		| latest			|
| 	redis		| latest			|
|	env_wxfine| v0.1				|
| 	lightweb	| v0.2				|
> 其中env_wxfine:v0.1和lightweb:v0.2需要制作，其他的几个可以直接 `$ docker pull xxx。`

### 2 制作wx_fine:v0.1镜像
> 在项目源代码中的requirement.txt给出了需要的包，开始编写Dockerfile。 

``` 
FROM python:3								
RUN pip install -r requirement.txt
```
>wx_fined的镜像制作比较简单。从python镜像开始，使用pip install 命令安装python的模块。

### 3 制作lightweb:v0.2镜像
> 

```
 FROM python:3
 ENV PYTHONUNBUFFERED 1
 ENV ORACLE_HOME /opt/oracle/instantclient_12_1
 ENV LD_RUN_PATH=$ORACLE_HOME
 COPY /docker_dep/instantclient/* /tmp/
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN \
   apt-get update -y && \
   apt-get upgrade -y && \
   apt-get dist-upgrade -y && \
   apt-get -y autoremove && \
   apt-get clean && \
   mkdir -p /opt/oracle && \
   apt-get install unzip && \
   apt-get install libaio1 && \
   apt-get install libaio-dev && \
   apt-get install libffi-dev && \
   apt-get install libssl-dev && \
   unzip "/tmp/instantclient*.zip" -d /opt/oracle && \
   ln -s $ORACLE_HOME/libclntsh.so.12.1 $ORACLE_HOME/libclntsh.so && \
   pip install cx_Oracle && \
   pip install -r requirements.txt -i https://pypi.douban.com/simple/ && \
   bash -c 'mkdir -pv /home/newlight/{request,response}'
```
> 因为auto_fetch需要连接oracle数据库，所以需要需要一个cx_oracle包，负责连接oracle。这个镜像的制作用到的命令比上一个多，其中一个目的就是为了安装cx_oracle包。

## 怎么写docker-compose.yml
### 1 编写wx_fine的docker-compose.yml
> docker-compose是docker的一个项目，负责各个镜像之间的联系通讯。

 ```
 version: '2.1'

services:
  nginx:									# 要启动的服务的名字，这里根据镜像的名字和镜像的功能来起名字。
    image: nginx:latest					# nginx服务从镜像nginx:latest启动。
    ports:
      - "8000:8000"						# 主机端口与docker内部端口的映射，如果端口被占用，可以使用其他端口，也可以lsof -i:8000，然后kell -p 8000。
    volumes:
#     - ./lightGateway/static/:/user/share/nginx/html/:ro											# 挂载主机的目录到docker镜像的内部目录，可以到镜像观望查看关于镜像的信息，最后的ro是这个目录下文件只读的意思。
      - ./static/:/static/:ro
      - ./wx_fine/deploy/nginx/wx_fine.conf:/etc/nginx/conf.d/my.conf
    depends_on:							# 这个ngixn服务启动时依赖那个服务，这里是web服务，所以docker会先启动启动web服务，然后再启动nginx服务。
      - web								# 这个名字是下面的web服务的名字，也就是web。
    links:								# 声明服务之间的通讯，在不暴漏各个服务端口的情况下，让服务之间进行通讯。
      - web:weblocal					# 这个名称是web服务hostname字段的值。

  web:
    image: env_wxfine:v0.1
    command: circusd wx_fine/deploy/circusd.ini
    hostname: weblocal
    volumes:
      - .:/code
      - ./static:/static
    ports:
      - "8000"
    links:
      - postgres:postgreshost
    depends_on:
      - postgres

  postgres:
    image: postgres:9.6
    hostname: postgreshost
    ports:
      - "5432:5432"
    volumes:
      - /tmp/wxfine_db:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres.lkj
      - POSTGRES_DB=wxfine
      - PGDATA=/var/lib/postgresql/data/wxfine
  worker:
    image: env_wxfine:v0.1
#    command: bash -c " && celery -A lightGateway beat -l info -S django"
    command: circusd wx_fine/deploy/celery-circusd.ini
    volumes:
      - .:/code
    links:
      - web:weblocal

 ```
 
> 这里有四个服务，分别是nginx、web、postgres、worker。
  
### 2 编写auto-fetch的docker-compose.yml
> 制作方法与上面的docker-compose.yml大同小异。

```
version: '2.1'

services:
  db:
    image: rabbitmq:3-management
    hostname: rabbit
    environment:
      - RABBITMQ_DEFAULT_USER=guest
      - RABBITMQ_DEFAULT_PASS=guest
    ports:
      - "5672:5672"
      - "15672:15672"
  redis:
    image: redis:latest
    hostname: redis
    volumes:
      - /var/redis:/data
    ports:
      - "6399:6379"
  nginx:
    image: nginx:latest
    ports:
      - "8001:8000"
    volumes:
#     - ./lightGateway/static/:/user/share/nginx/html/:ro
      - ./lightGateway/static/:/static/:ro
      - ./lightGateway/deploy/nginx/lightGateway.conf:/etc/nginx/conf.d/my.conf
    depends_on:
      - web
    links:
      - web:weblocal

  web:
    image: lightweb:v0.2
    command: circusd lightGateway/deploy/circusd.ini
    hostname: weblocal
    volumes:
      - .:/code
      - ./lightGateway/static:/static
      - /home/newlight/request/:/home/newlight/request/
      - /home/newlight/response/:/home/newlight/response/
    ports:
      - "8000"
    links:
      - db:rabbit
      - redis:redis
    environment:
      - LANG=C.UTF-8
    # - DJANGO_SETTINGS_MODULE=lightGateway.settings.develop
    depends_on:
      - redis

  # Celery worker
  worker:
    image: lightweb:v0.2
#   command: bash -c " && celery -A lightGateway beat -l info -S django"
    command: circusd lightGateway/deploy/celery-circusd.ini
    volumes:
      - .:/code
      - /home/newlight/request/:/home/newlight/request/
      - /home/newlight/response/:/home/newlight/response/
    links:
      - db:rabbit
      - web:weblocal
    depends_on:
      - db
      - web
```


