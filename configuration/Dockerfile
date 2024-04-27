FROM ubuntu:20.04
USER root
WORKDIR /app
COPY main.py /app/main.py
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    openvswitch-common \
    ifupdown \
    iproute2 \
    iptables \
    iputils-ping \
    net-tools \
    openvswitch-switch \
    openvswitch-testcontroller \
    python3-pip \
    mininet \
    sudo

RUN pip install mininet
RUN /usr/share/openvswitch/scripts/ovs-ctl start
RUN ovs-vsctl show

CMD ["sudo","python3", "main.py"]
