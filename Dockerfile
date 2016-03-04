FROM ubuntu:15.10
MAINTAINER Deepak Prabhakara email: deepak@redsift.io version: 1.1.101

ARG version=2.7

ENV PYTHONUNBUFFERED=1
ENV SIFT_ROOT="/run/dagger/sift" IPC_ROOT="/run/dagger/ipc"
LABEL io.redsift.dagger.init="/usr/bin/redsift/install.py" io.redsift.dagger.run="/usr/bin/redsift/bootstrap.py"

# TODO: This doesn't work if sift root is overridden when running the container.
ENV PYTHONPATH="$SIFT_ROOT/server/site-packages"

# Fix for ubuntu to ensure /etc/default/locale is present
RUN update-locale

RUN export DEBIAN_FRONTEND=noninteractive && \ 
  apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y \
	build-essential git pkg-config \
  python${version}-dev python${version} python-pip \
  libnanomsg-dev && \
  apt-get clean -y && \
	rm -rf /root/.pip/cache/* /tmp/pip* && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY root /
COPY vendor /vendor

RUN cd /vendor/nanomsg-python && python setup.py install

VOLUME /run/dagger/sift

WORKDIR /run/dagger/sift

ENTRYPOINT ["/usr/bin/python3"]
