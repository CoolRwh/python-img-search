FROM python:3.7.16

LABEL MAINTAINER="1016681491@qq.com"

# 切换镜像源
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN  apt-get clean && apt-get update

# 安装需要的 扩展
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx git-lfs -y


# 安装  python3-opencv
RUN apt-get install -y python3-opencv

WORKDIR /docker/data

# 设置镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN python -m pip install --upgrade pip
## 安装 扩展
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# CMD [ "python", "searchServer.py"]


RUN rm -rf /tmp/* /var/log/* /var/cache/*  /var/cache/* 

RUN touch /docker/log.txt

CMD ["tail","-f","/docker/log.txt"]