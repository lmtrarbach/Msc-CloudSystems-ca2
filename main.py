from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI

class CloudVPCTopo(Topo):
    def build(self):
        # Define switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Define hosts
        h1 = self.addHost('h1', ip='10.0.0.2/24')
        h2 = self.addHost('h2', ip='10.0.1.2/24')
        h3 = self.addHost('h3', ip='10.1.0.2/24')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(s1, s2)
        self.addLink(s2, h3)

def create_network():
    topo = CloudVPCTopo()
    net = Mininet(topo)
    net.start()

    # security groups
    h1, h2, h3 = net.get('h1', 'h2', 'h3')
    h1.cmd('iptables -A OUTPUT -p icmp --icmp-type echo-reply -j DROP')  # Deny ping replies from h1
    h2.cmd('iptables -A INPUT -p icmp --icmp-type echo-request -j DROP')  # Deny ping requests to h2
    h3.cmd('iptables -A INPUT -s 10.0.0.0/24 -j DROP')  # Deny  traffic from subnet 10.0.0.0/24 to h3

    CLI(net) 
    net.stop()

if __name__ == '__main__':
    create_network()
