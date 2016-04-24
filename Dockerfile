FROM quay.io/redsift/sandbox:latest
MAINTAINER Deepak Prabhakara email: deepak@redsift.io version: 1.1.101

ENV PYTHONUNBUFFERED=1

LABEL io.redsift.dagger.init="/usr/bin/redsift/install.py" io.redsift.dagger.run="/usr/bin/redsift/bootstrap.py"

RUN export DEBIAN_FRONTEND=noninteractive && \ 
  apt-get update && \
	apt-get install -y \
	build-essential git \
  python2.7-dev python2.7 python-pip && \
  apt-get clean -y && \
	rm -rf /root/.pip/cache/* /tmp/pip* && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY root /
COPY vendor /vendor

RUN cd /vendor/nanomsg-python && python setup.py install

RUN pip install -r /usr/bin/redsift/requirements.txt

ENTRYPOINT ["/usr/bin/python"]
