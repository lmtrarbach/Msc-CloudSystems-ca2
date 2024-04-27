import os
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time


def test_network_resilience(net):
    info("Should pass \n")
    s1, s2 = net.get('s1'), net.get('s2')
    net.pingAll()

    s1.config(loss=100)
    s2.config(loss=100)

    info("Shpuld fail\n")
    net.pingAll()

    s1.config(loss=0)
    s2.config(loss=0)


def setup_topology():
    floodlight_ip = "172.18.0.2"
    floodlight_port = 6653

    net = Mininet(controller=RemoteController)
    print(f"Starting Mininet with IP: {floodlight_ip} and port: {floodlight_port}")
    time.sleep(1)
    net.addController(
        controller=RemoteController,
        switch=OVSSwitch,
        link=TCLink,
        ip=floodlight_ip,
        port=floodlight_port,
        waitConnected=True,
    )
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")
    host1 = net.addHost("host1")
    host2 = net.addHost("host2")
    host3 = net.addHost("host3")
    host4 = net.addHost("host4")
    host5 = net.addHost("host5")

    net.addLink(host1, s1)
    net.addLink(host2, s1)
    net.addLink(host3, s1)
    net.addLink(host3, s2)
    net.addLink(host4, s2)
    net.addLink(host5, s2)

    net.start()


    # Test
    test_network_resilience(net)

    # Start CLI
    CLI(net)

    # Stop network
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    setup_topology()
