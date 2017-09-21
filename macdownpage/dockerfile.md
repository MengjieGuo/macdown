# dockerfile

这里都是使用python的模块，都是可以通过pip进行安装的。

```
FROM python:3.5
MAINTAINER guo
# ENV  VAR 1
RUN mkdir /code
WORKDIR /code
ADD ./requirements.txt /code/
RUN pip install -r requirements.txt
# VOLUMN ["/Users/screman/"]
CMD ["/bin/bash"]
# EXPOSE 80;

```

如果新增了python module

```
FROM guo/env_practice:v0.1
MAINTAINER guo
ADD ./requirements_plus.txt /code/
WORKDIR /code
RUN pip install -r requirements_plus.txt
```