import os
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time


def test_network_resilience(net):
    info("Testing - Should all pass\n")
    host4 = net.get("host4")
    # Testing with all working setup
    for each in range(1, 6):
        if each != 4:
            result = net.get(f"host{each}").cmd(f"ping -c 2 {host4}")
            if " 0% packet loss" in result:
                info(f"Connectivity between host4 and host{each} is successful \n")
            else:
                info(f"Connectivity between host4 and host{each} failed \n")

    net.get("host4").cmd("iptables -A INPUT -j DROP")

    info("Testing - Should fail")
    for each in range(1, 6):
        if each != 4:
            result = net.get(f"host{each}").cmd(f"ping -c 2 {host4}")
            if " 0% packet loss" in result:
                info(f"Connectivity between host4 and host{each} is successful \n")
            else:
                info(f"Connectivity between host4 and host{each} failed \n")


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
    host1 = net.addHost("host1")
    host2 = net.addHost("host2")
    host3 = net.addHost("host3")
    host4 = net.addHost("host4")
    host5 = net.addHost("host5")

    net.addLink(host1, s1)
    net.addLink(host2, s1)
    net.addLink(host3, s1)
    net.addLink(host4, s1)
    net.addLink(host4, s1)
    net.addLink(host5, s1)

    net.start()

    # Connect host4 directly to both switches
    net.addLink(host4, s1)

    # Test
    test_network_resilience(net)

    # Start CLI
    CLI(net)

    # Stop network
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    setup_topology()
