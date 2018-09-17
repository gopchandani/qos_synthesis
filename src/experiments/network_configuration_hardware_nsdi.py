__author__ = 'Rakesh Kumar'

import os, json
import networkx as nx
import paramiko
paramiko.util.log_to_file("filename.log")


class NetworkConfigurationHardwareNsdi(object):

    def __init__(self):
       self.graph = nx.DiGraph()

    def run_cmd_via_paramiko(self, IP, port, username, password, command):

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        s.connect(IP, port, username, password)
        (stdin, stdout, stderr) = s.exec_command(command)

        output = list(stdout.readlines())
        s.close()
        return output


    def clear_all_flows_queues(self):

        for switch_dict in self.switch_dict_iter():

            delete_flows_cmd = 'ovs-ofctl del-flows ' + 'tcp:' + str(switch_dict["switch_ip"]) + ':' + \
                            str(switch_dict["of_port"])

            os.system(delete_flows_cmd)

            delete_groups_cmd = 'ovs-ofctl -O OpenFlow13 del-groups ' + 'tcp:' + str(switch_dict["switch_ip"]) + ':' + \
                            str(switch_dict["of_port"])

            os.system(delete_groups_cmd)


            for port in switch_dict["port_list"]:

                port_clear_qos_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                            "clear Port " + port + " qos"
                os.system(port_clear_qos_cmd)


            destroy_qos_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                            "--all destroy qos"

            os.system(destroy_qos_cmd)

            destroy_queue_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                            "--all destroy queue"

            os.system(destroy_queue_cmd)

    def add_switches(self):
        switch_dict= {"switch_name": "ps1",
                      "bridge_name": "br0",
                      "switch_ip": "192.17.101.126",
                      "usr": "admin",
                      "psswd": "csl440",
                      "of_port": "6633",
                      "port_list":['ge-1/1/1','ge-1/1/2','ge-1/1/4']}

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps2",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.127",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list":['ge-1/1/2', 'ge-1/1/4', 'ge-1/1/6']}

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps3",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.128",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list": ['ge-1/1/2', 'ge-1/1/8', 'ge-1/1/10']}

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps4",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.129",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list": ['ge-1/1/2', 'ge-1/1/4', 'ge-1/1/1']}

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)


    def is_switch(self, node_id):
        if self.graph.node[node_id]["node_type"] == "switch":
            return True
        else:
            return False

    def is_host(self, node_id):
        if self.graph.node[node_id]["node_type"] == "host":
            return True
        else:
            return False



    def get_host_dict(self, host_id):
        return self.graph.node[host_id]['h']

    def get_switch_dict(self, switch_id):
        return self.graph.node[switch_id]['b']

    def get_link_dict(self, node1_id, node2_id):
        return self.graph[node1_id][node2_id]['l']

    def add_host_nodes(self):

        host_dict = {"host_name": "dot08",
                     "switch_id" : "ps1",
                     "host_ip": "192.168.1.8",
                     "mgmt_ip": "10.192.180.112",
                     "usr": "pi",
                     "psswd": "raspberry"
            }

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

        host_dict = {"host_name": "dot09",
                     "switch_id": "ps4",
                     "host_ip": "192.168.1.9",
                     "mgmt_ip": "10.193.188.190",
                     "usr": "pi",
                     "psswd": "raspberry"
                     }

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

    def switch_attached_host_dicts(self,switch_dict):
        host_dict_list=[]

        for host_dict in self.host_dict_iter():
                if host_dict["switch_id"] == switch_dict["switch_name"]:
                    host_dict_list.append(host_dict)

        return host_dict_list

    def host_dict_iter(self):
        for node_id in self.graph.node():

            if self.graph.node[node_id]['node_type'] == "host":
                yield self.graph.node[node_id]['h']

    def switch_dict_iter(self):
        for node_id in self.graph.node():

            if self.graph.node[node_id]['node_type'] == "switch":
                yield self.graph.node[node_id]['b']

    def get_node_type(self, node_id):
        node_type = None

        if self.graph.has_node(node_id):
            node_type = self.graph.node[node_id]["node_type"]

        return node_type

    def add_host_links(self):

        pi_to_switch_bw = 1000000 * 50 #Assume pi to switch bandwidth is 50 Mbps
        pi_to_switch_delay = 10e-6 * 10 # Assumes pi to switch latency is 10 microseconds

        links = [("dot08", "ps1", "eth0", "ge-1/1/1", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot09", "ps4", "eth0", "ge-1/1/1", "host-sw", pi_to_switch_bw, pi_to_switch_delay)]

        self.add_links(links)


    def add_links(self, links):
        for node1, node2, node1_port, node2_port, link_type, bw, delay in links:
            link_dict = {
                "node1": node1,
                "node2": node2,
                "node1_port": node1_port,
                "node2_port": node2_port,
                "bw": bw,
                "delay":delay
            }

            self.graph.add_edge(link_dict["node1"],
                                link_dict["node2"],
                                l=link_dict, t=link_type)
            link_dict = {
                "node1": node2,
                "node2": node1,
                "node1_port": node2_port,
                "node2_port": node1_port,
                "bw": bw,
                "delay": delay
            }

            self.graph.add_edge(link_dict["node1"],
                                link_dict["node2"],
                                l=link_dict, t=link_type)

    def add_switch_links(self):

        switch_to_switch_bw = 1000000 * 1000 * 10  # Assume pi to switch bandwidth is 10 Gbps
        switch_to_switch_delay = 10e-9 * 10  # Assumes pi to switch latency is 10 nanoseconds

        links = [("ps1", "ps2", "ge-1/1/2", "ge-1/1/2","sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                 ("ps1", "ps3", "ge-1/1/4", "ge-1/1/2","sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                 ("ps2", "ps3", "ge-1/1/4", "ge-1/1/8","sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                 ("ps2", "ps4", "ge-1/1/6", "ge-1/1/2", "sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                 ("ps3", "ps4", "ge-1/1/10", "ge-1/1/4","sw-sw", switch_to_switch_bw, switch_to_switch_delay)]

        self.add_links(links)


    def setup_network_configuration(self):

        # These things are needed by network graph...
        self.add_host_nodes()
        self.add_switches()
        self.add_host_links()
        self.add_switch_links()
        self.clear_all_flows_queues()


