#__author__ = 'Monowar Hasan'
# from __future__ import division
import networkx as nx
import sys
from collections import defaultdict
import math
import pandas as pd
import random

from model.intent import Intent
from synthesis.synthesis_lib import SynthesisLib

from copy import deepcopy

class MCP_Helper(object):

    def __init__(self, nw_graph, hmax, delay_budget, bw_budget, bw_req_flow, x=10):
        self.nw_graph = nw_graph
        self.x = x
        self.d = defaultdict(dict)
        self.pi = defaultdict(dict)

        # this are for testing purposes only
        #self.hmax = 3 # TO DO: need to calculate from the graph
        self.hmax = hmax

        #self.bw_req_flow = 50 # MBPS
        self.bw_req_flow = bw_req_flow

        #self.link_bw = 100 # MBPS

        #self.bw_utilization = float(self.bw_req_flow) / float(self.link_bw)
        #self.link_delay = 3 # ms

        #self.delay_budget = 100 # ms
        self.delay_budget = delay_budget
        self.bw_budget = bw_budget

        #print "BW utilization {}".format(self.bw_utilization)

    def init_mcp(self, src, itr):
        # print 'print nodes'
        # print nw_graph.nodes()
        if itr == 1:
            loop_range = self.x
        elif itr == 2:
            loop_range = int(math.floor(self.bw_budget))
        else:
            raise NotImplementedError

        for v in self.nw_graph.nodes():
            #for i in range(self.x + 1):
            for i in range(loop_range + 1):
                self.d[v][i] = float("inf")
                # self.d[v][i] = 100000000000 # a very big number
                # self.d[v][i] = 0
                self.pi[v][i] = float("nan")

        for i in range(self.x + 1):
            self.d[src][i] = 0.0

        # print self.d

    def get_bandwidth(self, u, v):

        '''

        if (u=="s" and v=="u") or (v=="s" and u=="u"):
            return 1.0
        elif (u=="s" and v=="v") or (v=="s" and u=="v"):
            return 1.0
        elif (u == "u" and v == "t") or (v == "u" and u == "t"):
            return 2.5
        elif (u == "u" and v == "v") or (v == "u" and u == "v"):
            return 1.0
        elif (u == "v" and v == "t") or (v == "v" and u == "t"):
            return 4.0
        else:
            raise NotImplementedError
        '''

        # return self.bw_utilization
        # return 0.5
        # return random.random()
        return float(self.bw_req_flow) / float(self.nw_graph[u][v]['link_bw'])

    def get_new_bandwidth(self, u, v):

        # bw_util = float(self.bw_req_flow) / float(self.nw_graph[u][v]['link_bw'])
        #C = self.hmax * self.bw_utilization
        # C = self.hmax * bw_util
        # return math.ceil((self.get_bandwidth(u, v) * self.x) / C)
        return math.ceil((self.get_bandwidth(u, v) * self.x) / self.bw_budget)

    def get_delay(self, u, v):

        # return 3.0 / 100.0
        # return self.link_delay/float(self.delay_budget)

        # return self.link_delay

        return self.nw_graph[u][v]['link_delay']

    def get_new_delay(self, u, v):

        '''
        if (u=="s" and v=="u") or (v=="s" and u=="u"):
            return 6.0
        elif (u=="s" and v=="v") or (v=="s" and u=="v"):
            return 10.0
        elif (u == "u" and v == "t") or (v == "u" and u == "t"):
            return 5.0
        elif (u == "u" and v == "v") or (v == "u" and u == "v"):
            return 3.0
        elif (u == "v" and v == "t") or (v == "v" and u == "t"):
            return 1.0
        else:
            raise NotImplementedError

        '''

        return math.ceil((self.get_delay(u, v) * self.x) / float(self.delay_budget))

        # return 3.0
        # return random.random()

    def relax_mcp(self, u, v, k, itr):

        if itr == 1:
            w1 = self.get_delay(u,v)
            w2_prime = self.get_new_bandwidth(u,v)
            loop_range = self.x

            # w1 = self.get_bandwidth(u, v)
            # w2_prime = self.get_new_delay(u, v)
            #print "(delay) = {}, (new-bw) = {}".format(w1, w2_prime)
        elif itr == 2:
            w1 = self.get_new_delay(u, v)
            w2_prime = self.get_bandwidth(u, v)
            loop_range = int(math.floor(self.bw_budget))
            # print "(new-delay) = {}, (bw) = {}".format(w1, w2_prime)

            # smruti
            #w1 = self.get_bandwidth(u, v)
            #w2_prime = self.get_new_delay(u, v)
            #print "w1 (bw) = {}, w2prime (nw-delay) = {}".format(w1, w2_prime)

            # w1 = self.get_new_bandwidth(u, v)
            # w2_prime = self.get_delay(u, v)

        else:
            raise NotImplementedError

        kprime = int(k + w2_prime)  # print "kprime is {}".format(kprime)
        # print "u, v is ({}, {})".format(u, v)
        # print "kprime:{}, w1({},{})={}, w2_prime({},{})={}".format(kprime, u, v, w1, u, v, w2_prime)
        # print "d[{}][{}] = {}, d[{}][{}] + w1 = {}".format(v,kprime, self.d[v][kprime], u, k, self.d[u][k] + w1)

        #if kprime <= self.x:
        if kprime <= loop_range:
            #print "kprime is {}".format(kprime)
            # print "(v, u):({},{}) - {} -> {}".format(v, u, self.d[v][kprime], self.d[u][k] + w1)
            if self.d[v][kprime] > self.d[u][k] + w1:
                #print "in if"
                self.d[v][kprime] = self.d[u][k] + w1
                self.pi[v][kprime] = u
                # print "== kprime {}, {} -> {}  ==".format(kprime, v, u)

                # print "this line"

    def calculate_mcp_ebf(self, src, dst, itr):
        print "== Calculating MCP_EBF==="

        if itr == 1:
            loop_range = self.x
        elif itr == 2:
            loop_range = int(math.floor(self.bw_budget))
        else:
            raise NotImplementedError

        self.init_mcp(src, itr)

        number_of_nodes = len(list(self.nw_graph.nodes()))
        for i in range(1, number_of_nodes):
        # for i in range(number_of_nodes):
            # for k in range(self.x+1):
            for k in range(loop_range+1):
                for edge in self.nw_graph.edges():
                    u = edge[0]
                    v = edge[1]
                    self.relax_mcp(u, v, k, itr)

    def extract_path(self, src, dst, itr):

        path = []
        traverse_done = False
        current_node = dst

        if itr == 1:
            loop_range = self.x
        elif itr == 2:
            loop_range = int(math.floor(self.bw_budget))
        else:
            raise NotImplementedError

        count = 0
        maxcount  = 1000000 # some arbitrary large number
        while not traverse_done:
            #for k in range(self.x + 1):
            count = count + 1
            if count > maxcount:
                raise ValueError('Unable to find path within maximum timeout')

            for k in range(loop_range + 1):
                if not pd.isnull(self.pi[current_node][k]):
                    path.append(current_node)
                    current_node = self.pi[current_node][k]
                    break
                if current_node == src:
                    path.append(current_node)
                    traverse_done = True
                    break

        return path

    def check_solution(self, dst, itr):
        if itr == 1:
            c1 = self.delay_budget
        elif itr==2:
            c1 = self.x
        else:
            raise NotImplementedError

        for k in range(self.x+1):
            if self.d[dst][k] <= c1:
                return True

        return False

    def get_path_layout(self, src, dst):
        path_src_2_dst =  []
        itr = 2
        for i in range(1, itr + 1):
            # print "iteration {}".format(i)

            self.calculate_mcp_ebf(src, dst, i)

            if self.check_solution(dst, i):
                print "Path found at pass {}".format(i)
                path = self.extract_path(src, dst, i)
                path_src_2_dst = path[::-1]
                # print path_src_2_dst
                # break
                return path_src_2_dst
            else:
                print "Unable to find path at pass {}".format(i)

        return path_src_2_dst


def print_graph(nw_graph):

    print "print nodes.."
    #print(list(nw_graph.nodes()))
    print nw_graph.nodes()

    print "print edges..."
    # print(list(nw_graph.edges()))
    print nw_graph.edges()

    '''
    print 'adjacency matrix'
    nx.write_adjlist(nw_graph, sys.stdout)  # write adjacency list to screen
    print 'end adjacency matrix'
    '''


def get_bw_budget(nw_config, bw_req_flow, hmax):
    max_bw_util = 0
    nw_graph = nw_config.ng.get_node_graph()
    for i in nw_graph.edges():
        ld = nw_config.ng.get_link_data(i[0], i[1])
        link_bw = ld.link_bw
        bw_util = hmax * float(bw_req_flow) / float(link_bw)
        # bw_util = hmax * float(bw_req_flow) / float(nw_graph[i[0]][i[1]]['link_bw'])
        if bw_util >= max_bw_util:
            max_bw_util = bw_util

    return max_bw_util


def calibrate_graph(nw_config):

    nw_graph = nx.DiGraph()
    graph = nw_config.ng.get_node_graph()

    for i in graph.nodes():
        nw_graph.add_node(i)

    # create bidirectional links
    for i in graph.edges():
        ld = nw_config.ng.get_link_data(i[0], i[1])
        link_delay = ld.link_delay
        link_bw = ld.link_bw
        # link_delay = graph[i[0]][i[1]]['link_delay']
        # link_bw = graph[i[0]][i[1]]['link_bw']
        nw_graph.add_edge(i[0], i[1], link_delay=link_delay, link_bw=link_bw)
        nw_graph.add_edge(i[1], i[0], link_delay=link_delay, link_bw=link_bw)

    return nw_graph


def calculate_hmax(nw_graph):

    hmax = nx.number_of_nodes(nw_graph)

    # print "hmax  is {}".format(hmax)
    return hmax


def compute_path_intents(network_graph, fs):

    intent_list = []

    # Get the port where the host connects at the first switch in the path
    link_ports_dict = network_graph.get_link_ports_dict(fs.ng_src_host.node_id, fs.ng_src_host.sw.node_id)
    in_port = link_ports_dict[fs.ng_src_host.sw.node_id]

    # This loop always starts at a switch
    for i in range(1, len(fs.path) - 1):

        link_ports_dict = network_graph.get_link_ports_dict(fs.path[i], fs.path[i+1])

        fwd_flow_match = deepcopy(fs.flow_match)
        mac_int = int(fs.ng_dst_host.mac_addr.replace(":", ""), 16)
        fwd_flow_match["ethernet_destination"] = int(mac_int)

        intent = Intent("primary",
                        fwd_flow_match,
                        in_port,
                        link_ports_dict[fs.path[i]],
                        True,
                        min_rate=fs.configured_rate_bps,
                        max_rate=fs.configured_rate_bps)

        # Store the switch id in the intent
        intent.switch_id = fs.path[i]

        intent_list.append(intent)
        in_port = link_ports_dict[fs.path[i+1]]

    return intent_list


def synthesize_flow_specifications(nc):

    synthesis_lib = SynthesisLib("localhost", "8181", nc.ng)

    print "Synthesizing rules and queues in the switches..."

    for fs in nc.flow_specs:

        # Compute intents for the path of the fs
        intent_list = compute_path_intents(nc.ng, fs)

        # Push intents one by one to the switches
        for intent in intent_list:
            synthesis_lib.push_destination_host_mac_intent_flow_with_qos(intent.switch_id, intent, 0, 100)


def find_path_by_mcp(nw_config, x=10):
    nw_graph = nw_config.ng.get_node_graph()

    for current_flow in nw_config.flow_specs:
        # current_flow = nw_config.flow_specs[0]
        bw_req_flow = current_flow.configured_rate_bps

        hmax = calculate_hmax(nw_graph)
        src = current_flow.src_host_id
        dst = current_flow.dst_host_id
        delay_budget = current_flow.delay_budget

        bw_budget = get_bw_budget( nw_config, bw_req_flow, hmax)
        # print "BW budget = {}".format(bw_budget)
        # hmax = 3

        # print_graph(nw_graph)

        # print "=== after calibration === "
        nw_graph = calibrate_graph(nw_config)
        # print_graph(nw_graph)

        mh = MCP_Helper(nw_graph, hmax, delay_budget, bw_budget, bw_req_flow, x)
        path = mh.get_path_layout(src, dst)
        #return path
        #'''
        if not path:
            print "No path found for flow {} to {}".format(current_flow.src_host_id, current_flow.dst_host_id)
        else:
            print "Path found for flow {} to {}".format(current_flow.src_host_id, current_flow.dst_host_id)
            print path
            # set the path for the flow
            current_flow.path = path
        #'''

