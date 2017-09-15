# The General Procedure for Setting Up a Autonomous Deploy Environment for Production

## CentOS Installation
* Check for minimal installation or server installation

## Install Docker Locally using YUM with internet access
You can use the Ali cloud installation script, because the official script will be slower
> ```
> $ curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
> ```


update yum software source, and install docker-engine.
> $ sudo yum update
> 
> $ sudo yum install docker-engine

Start Docker engine.
> $ sudo systemctl enable docker
> 
> $ sudo systemctl start docker

You must add group and user.
> $ sudo groupadd docker
> 
> $ sudo usermod -aG docker $USER

$USER is you username.

Of course, you can not use the installation script, the manual installation


## Export Docker rpm with dependency
* reoptrack comes with rescure to generate all the depencencies for docker installation
* Repotrack can download the software we want to install and its dependencies. All the packages will be downloaded to the current directory, so every time you use repotrack to build a directory, and then use the directory in the repotrack.

download our packages.

> ```
> $ mkdir docker_repo
> 
> $ cd docker_repo
> 
> $ repotrack docker
> ```

And then... waiting for download to complete.
> ```
> $ cd ../  
> 
> $ tar -cvf docker_repo.tar docker_repo
> ```

Send our packets to the destination host, of course, to be connected through the network.
> ```
> scp docker_repo.tar remote_username@remote_ip:remote_folder
> ```

No accident, the software package to the target host

https://www.linuxquestions.org/questions/linux-newbie-8/yum-local-install-package-and-all-dependencies-in-local-directory-774565/

## Install rpm Remotely on the serve without Internet access
* 'yum localinstall' is for one package.
* Dependencies will be downloaded from the enabled repositories only.

* For local dependencies :
    rpm -Uvh *
** when the package + all dependencies are in the same directory.

* 'rpm -ivh' is used when you want to have two versions of the same library installed.
* ( Or if you are absolutely sure that no package by the same name is installed.)
* Yum always uses 'rpm -Uvh' for install

You can now use localinstall to install the docker. Of course, you must in the docker_repo directory.
> ```
> $ yum localinstall docker_rpm_name
> ```

Here may encounter a software conflict, that is, has installed a software package, but now have to install a different version. According to the tips - skip. You also may 

Next step is add a group docker, add user to docker group and start docker.
> groupadd docker 
> 
> usermod -a -G docke USER_NAME
> 
> service docker start
>

If you want docker to start with computer. Of course docker must be a service.
> systemctl enable docker
 

## Build local Docker Image for Application Running Environmnet

The mirror is made based on our project to make our project based on the python language when the Django project.

The module required for the project can generally be installed through the python pip, just like we do `pip install redis`. The module required for the project can generally be installed through the python pip. Here we need to connect to the Oracle database python module, unfortunately, there seems to be no way to install through `pip install Cx_oracle` in python image easily.
> ```
>  FROM python:3     				        # our basic image
 ENV PYTHONUNBUFFERED 1	 				  # variable
 ENV ORACLE_HOME /opt/oracle/instantclient_12_1 # variable
 ENV LD_RUN_PATH=$ORACLE_HOME # variable
 COPY /docker_dep/instantclient/* /tmp/   # copy all things to /tmp/
 RUN mkdir /code 						  # make a dir /code 

>  WORKDIR /code 							# change dir to /code
 ADD requirements.txt /code/			  # just like copy, so we can use pip install -r requirements.txt
 RUN \									  #  RUN means to run a order, there we update our software
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
> ```

Next, we can use dockerfile to build our image. The `.` is required.
> $ docker build -t ourimage:v0.1 .

OK, we rename a image for our project, we tag it `ourimage:v0.1 `
>$ docker tag image_id someimage:v0.1

If you find a project that requires new modules to meet new features, you can use it like this. Also it is a python module.
> ```
> FROM ourimage:v0.1
> RUN pip install protobuf 
> ```

also
> $ docker build -t ourimage:v0.2 .

## Install the Docker Image on the Remote Server

Other mirrors, like nginx, redis, python, rabbimq we can directly use the docker pull name to get. Just like this. 
> $ docker pull nginx:latest
> 
> $ docker pull postgres:v9.6

You can not give the tag, it will download the latest one.
> $ docker pull redis

It will worker like..
> $ docker pull redis:latest 

Here, we have docker, images, you can pass the image to the destination host, and import our image, of course, first step is the local export.
> $ docker save -o aname.tar image_id

And trans `anama.tar` to the Remote host.
> $ scp aname.tar remote_username@remote_ip:remote_dir

Now, in the Remote host. Changer workspacd to where aname.tar in.
> $ docker load -i aname.tar

You can use like this.
> $ docker load < aname.tar

To see the iamge we load.
> $ docker images

But, it may be have no name, it only has image_id. You can tag it.
> $ docker tag aname:v0.2 image_id

Next, we can test if the image is work. The best practice is to pass the local test after passing to the remote host.

## Test the Docker Container by Loading the Image


