import os
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

def test_network_resilience(net):
    info("Testing - Should all pass")
    # Testing with all working setup
    net.pingAll()
    # Drop connection between host1 and host2
    net.get('h1').cmd('iptables -A OUTPUT -s 10.0.0.1 -d 10.0.0.2 -j DROP')
    net.get('h2').cmd('iptables -A OUTPUT -s 10.0.0.2 -d 10.0.0.1 -j DROP')

    # Test connectivity after dropping 
    info("Testing - Should fail")
    net.pingAll()

    # Restore connections
    net.get('h1').cmd('iptables -D OUTPUT -s 10.0.0.1 -d 10.0.0.2 -j DROP')
    net.get('h2').cmd('iptables -D OUTPUT -s 10.0.0.2 -d 10.0.0.1 -j DROP')


def setup_topology():
    floodlight_ip = "172.18.0.2"
    floodlight_port = 6653

    net = Mininet(controller=RemoteController)
    print(f'Starting mininet with IP: {floodlight_ip} and port: {floodlight_port}')
    time.sleep(1)
    net.addController(controller=RemoteController,switch=OVSSwitch, link=TCLink, ip=floodlight_ip, port=floodlight_port, waitConnected=True)
    s1 = net.addSwitch('s1')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.start()

    # Test 
    test_network_resilience(net)


    # Start CLI
    CLI(net)

    # Stop network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_topology()
