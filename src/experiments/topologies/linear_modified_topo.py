__author__ = 'Rakesh Kumar'

from mininet.topo import Topo


class LinearModifiedTopo(Topo):
    
    def __init__(self, params):
        
        Topo.__init__(self)
        
        self.params = params
        self.total_switches = self.params["num_switches"]
        self.switch_names = []

        #  Add switches and hosts under them
        for i in xrange(self.params["num_switches"]):
            curr_switch = self.addSwitch("s" + str(i+1), protocols="OpenFlow14")
            self.switch_names.append(curr_switch)

            for j in xrange(self.params["num_hosts_per_switch"]):
                curr_switch_host = self.addHost("h" + str(i+1) + str(j+1))
                self.addLink(curr_switch, curr_switch_host)

    def get_switches_with_hosts(self):
        return self.switch_names

    def __str__(self):
        params_str = ''
        for k, v in self.params.items():
            params_str += "_" + str(k) + "_" + str(v)
        return self.__class__.__name__ + params_str
