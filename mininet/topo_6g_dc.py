from mininet.topo import Topo

class DC6GTopo(Topo):
    def build(self):
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")

        self.addLink(h1, s1, bw=100, delay="1ms")
        self.addLink(h2, s1, bw=80, delay="2ms")
        self.addLink(h3, s2, bw=60, delay="3ms")
        self.addLink(s1, s2, bw=70, delay="2ms")

topos = {"dc6g": DC6GTopo}
