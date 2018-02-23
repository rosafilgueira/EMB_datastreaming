FROM docker.elastic.co/elasticsearch/elasticsearch-platinum:6.2.1

RUN \
  yum install -y \
                  python-setuptools \
                  hostname \
                  yum-utils \
yum clean all && \
easy_install supervisor

RUN yum install -y net-tools python

# Add scripts
ADD scripts/create-index.sh /usr/bin/create-index.sh

RUN mkdir /opt/create-es-index
RUN yum -y install vim 

ADD scripts/__init__.py /opt/create-es-index/__init__.py
ADD scripts/es_config.py  /opt/create-es-index/es_config.py
ADD scripts/es_create_index.py  /opt/create-es-index/es_create_index.py
ADD scripts/es_drop.py /opt/create-es-index/es_drop.py
ADD scripts/check_index.sh /opt/create-es-index/check_index.sh
ADD scripts/check_values.sh /opt/create-es-index/check_values.sh

# Supervisor config

RUN echo_supervisord_conf > /usr/etc/supervisord.conf

ADD supervisor/start-elasticsearch.conf supervisor/create-index.conf /etc/supervisor/conf.d/

RUN echo "[include]" >> /usr/etc/supervisord.conf

RUN echo "files = /etc/supervisor/conf.d/*.conf" >> /usr/etc/supervisord.conf

RUN chown -R elasticsearch:elasticsearch /tmp/

CMD ["supervisord", "-n"]
