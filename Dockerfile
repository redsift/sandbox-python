FROM python:2

LABEL io.redsift.dagger.init="install.py" io.redsift.dagger.run="bootstrap.py"
ENV SIFT_ROOT="test_sift" IPC_ROOT="/run/dagger/ipc"

RUN apt-get update && \
    apt-get install -y libnanomsg-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY vendor /app/vendor
WORKDIR /app/vendor/nanomsg-python
RUN python setup.py install

COPY . /app
WORKDIR /app

ENTRYPOINT ["/usr/local/bin/python"]
