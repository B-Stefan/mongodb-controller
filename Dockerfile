FROM centos:7

MAINTAINER Stefann Bieliauskas<os@conts.de>

RUN yum -y install git epel-release && yum -y install python-pip && yum clean all && rm -rf /var/cache/yum
RUN pip install --upgrade pip setuptools && pip install git+git://github.com/kubernetes-incubator/client-python.git

ADD controller.py /tmp
ADD mongo-user.yml /tmp

ENTRYPOINT  ["python", "-u", "/tmp/controller.py"]
