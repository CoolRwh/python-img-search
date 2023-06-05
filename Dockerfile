FROM python:3.7.16

LABEL MAINTAINER="1016681491@qq.com"

# 切换镜像源
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN  apt-get clean && apt-get update

# 安装需要的 扩展
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx -y


# 安装  python3-opencv
RUN apt-get install -y python3-opencv

WORKDIR /docker/data

COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com


# RUN pip install torch==1.13.1 -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
# RUN pip install torchvision==0.14.1 -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com


# CMD [ "python", "searchServer.py"]


RUN rm -rf /tmp/* /var/log/* /var/cache/*  /var/cache/* 

RUN touch /docker/log.txt

CMD ["tail","-f","/docker/log.txt"]