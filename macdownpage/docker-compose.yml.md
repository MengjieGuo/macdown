# docker-compose.yml
编写docker-compose.yml文件需要
注意代理环境变量和数据库环境变量
注意启动web和celery worker的命令改为了circus启动。

```
version: '0.1'
# 需要postgres数据库存储数据结构和数据。
# 需要redis存储临时数据，这些数据可能需要存储很久。
# 需要nginx作为http服务。
# 需要guo/env_practice:v0.2作为项目的运行环境
# 需要guo/env_practice:v0.2作为celery异步任务的环境。

# 设置各自的环境变量

service:

# 1、environment关键字设置容器使用的环境变量，也可以使用  env_file: - web-variables.env
#    在setting中有个部分用来配置项目的数据库信息
#        'NAME': 'wxfine',
#        'USER': 'postgres',
#        'PASSWORD': 'postgres.lkj',
#        'HOST': 'postgreshost',
#        'PORT': '5432',
# 2、需要存储数据和表结构，挂载目录  主机目录:postgres目录，这个postgres的数据目录怎么获得？找到你所使用的postgre镜像的制作dockerfile，
#    在dockerfile中会有RUN mkdir -p /var/lib/postgresql/data这样的语句。当然也可以自己制作一个postgres镜像。或者更改它的数据目录。
# 3、postgres被我们的web_practice需要，因为要使用postgres存储数据。有时我们需要从外部查看数据库信息，所以需要暴露端口。外面的端口随意，
#    里面的端口一般是5432，从你所使用的postgre镜像的制作dockerfile中会有EXPOSE 5432这样的语句。
# https://github.com/docker-library/postgres/blob/master/9.6/Dockerfile
  postgres:
    image: postgres:latest
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres.lkj
      - POSTGRES_HOST=postgreshost
      - POSTGRES_NAME=wxfine
      - PGDATA=/var/lib/postgresql/data/wxfine                          # 这个变量是数据库wxfine的数据所在目录
    volumn:
      - /home/guo/postdata:/var/lib/postgresql/data
    post:
      - '5432:5432'

#  redis:
#    image: redis:latest

# 1、http服务程序，需要暴露端口
# 2、nginx需要依赖web服务
  nginx:
    image: nginx: latest
    port:
      - '8000:8000'
    volumes:
#     - ./lightGateway/static/:/user/share/nginx/html/:ro
      - ./static/:/static/:ro                                           # 静态资源挂砸，nginx需要返回静态资源吗
      - ./wx_fine/deploy/nginx/wx_fine.conf:/etc/nginx/conf.d/my.conf   # 配置文件，为什么呢
                                                                        # 进入nginx容器，可以看到/etc/nginx/conf.d/有一个default.conf的配置文件
    depends_on:
      - web_practice
    links:
      - web_practice

# 1、启动web服务，依赖数据库postgres depends_on说明service之间的依赖，link除了service直接的依赖还可以告诉容器与哪个容器通信，
#    而不管对方容器的端口
# 2、项目需要写日志文件，我们每天需要获得这些日志文件，可以使用volumn，注意右边的目录是docker内部的目录，项目写日志时使用
#    /code/web_practice，所有在这个目录下的日志都会出现在/var/log/web_practice中，可以在服务器中看到。
# 3、项目使用正向代理时需要为容器指定代理，在服务器中全局指定是不行的
# https://stackoverflow.com/questions/35832095/difference-between-links-and-depends-on-in-docker-compose-yml
  web_practice:
    image: guo/env_practice:v0.2
#    commands: python manage.py runserver 0.0.0.0:8000
    commands: circusd wx_fine/deploy/circusd.ini        # circusd命令+配置文件名
                                                        # 启动服务，这里使用circus代替启动命令，circus有什么作用
                                                        # circues是进程和socket管理程序，
                                                        # circus参考https://circus.readthedocs.io/en/latest/
                                                        # gunicorn --workers=2 --bind 0.0.0.0:8000 wx_fine.wsgi
                                                        # gunicorn 是python WSGI webserver ，通常用来启动django应用程序
                                                        # gunicorn有什么用http://www.cnblogs.com/ArtsCrafts/p/gunicorn.html
                                                        # 使用参考http://docs.gunicorn.org/en/stable/settings.html
    volumn:
      - /var/log/web_practice:/var/web_practice/        # 挂载日志目录
      - ./:/code                                        # 挂载代码目录
      - ./static:/static                                # 挂载静态文件目录
    port:
      - '8000'                                          # 暴露端口8000
    environments:
      - http_proxy=username:passwd@ip:port              # 这里的porxy环境变量配置还是需要的
      - https_proxy=username:passwd@ip:port
    depends_on:
      - postgres
    links:
      - postgres

  worker_practice:
    image: guo/env_practice:v0.2
    commands: circusd wx_fine/deploy/celery-circusd.ini # 使用circus作为替代启动命令，怎么增加worker数量，队列，分优先级
    volumn:
      - ./:/code
      - /var/picture:/var/picture                       # 异步任务存储图片
    environments:
      - http_proxy=username:passwd@ip:port
      - https_proxy=username:passwd@ip:port
    depends_on:
      - postgres
    links:
      - postgres



```