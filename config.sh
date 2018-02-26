#!/bin/bash
set -x

sudo yum install -y yum-utils device-mapper-persistent-data lvm2

sudo yum-config-manager -y --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo yum-config-manager -y --enable docker-ce-edge

sudo yum-config-manager -y --enable docker-ce-test

sudo yum -y install docker-ce

sudo systemctl start docker

sudo yum -y  install epel-release

sudo yum -y install python-pip

sudo pip install --upgrade pip

sudo pip install docker-compose

sudo pip install elasticsearch
