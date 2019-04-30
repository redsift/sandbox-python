FROM quay.io/redsift/sandbox:latest
MAINTAINER Deepak Prabhakara email: deepak@redsift.io version: 1.1.102

ENV PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8

LABEL io.redsift.sandbox.install="/usr/bin/redsift/install.py" io.redsift.sandbox.run="/usr/bin/redsift/run.py"

COPY root /
COPY vendor /vendor

ARG v=2.7
ARG t=

ENV version=${v} tag=${t}
ENV PYTHONPATH=$PYTHONPATH:$HOME/lib/python PATH=$PATH:$HOME/lib/python

RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
	apt-get install -y \
	build-essential git \
  python$version-dev python$version python$tag-pip && \
  chown -R root:root $HOME && \
  pip$tag install -U pip || true && \
  apt-get purge -y && \
	rm -rf /root/.pip/cache/* /tmp/pip*

RUN pip$tag --version

RUN pip$tag install --user -r /usr/bin/redsift/requirements.txt

RUN chown -R sandbox:sandbox $HOME

ENTRYPOINT ["/usr/bin/python"]
