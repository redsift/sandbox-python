FROM quay.io/redsift/sandbox:20.04
MAINTAINER Christos Vontas email: christos@redsift.io version: 1.1.102

ENV PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8

LABEL io.redsift.sandbox.install="/usr/bin/redsift/install.py" io.redsift.sandbox.run="/usr/bin/redsift/run.py"

COPY root /

ARG v
ARG t

# Fail if args are missing
RUN test ${v}
RUN test ${t}

ENV version=${v} tag=${t}
ENV PYTHONPATH=$PYTHONPATH:$HOME/lib/python PATH=$PATH:$HOME/lib/python
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes
RUN curl https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add -
RUN echo 'deb https://apt.kitware.com/ubuntu/ focal main' > /etc/apt/sources.list.d/cmake.list
RUN apt update
RUN apt install -y build-essential cmake git s3cmd
RUN apt install -y python$version python$version-dev python$version-venv python$version-distutils
RUN python$version -m ensurepip --upgrade

RUN chown -R root:root $HOME
RUN ln -fs /usr/bin/python${v} /usr/bin/python3 && \
  apt purge -y && \
  rm -rf /root/.pip/cache/* /tmp/pip*

# Update outdated installed packages and requirements
RUN pip3 list -o 2>/dev/null | sed -n '3,${s/\s.*$//p}' | xargs -n 1 pip3 install -U  || true
RUN python$version -m pip install --user -r /usr/bin/redsift/requirements.txt

RUN chown -R sandbox:sandbox $HOME

ENTRYPOINT ["/usr/bin/python"]
