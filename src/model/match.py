__author__ = 'Rakesh Kumar'

import sys
from netaddr import IPNetwork
from UserDict import DictMixin

field_names = ["in_port",
              "ethernet_type",
              "ethernet_source",
              "ethernet_destination",
              "src_ip_addr",
              "dst_ip_addr",
              "ip_protocol",
              "tcp_destination_port",
              "tcp_source_port",
              "udp_destination_port",
              "udp_source_port",
              "vlan_id",
               "has_vlan_tag"]

ryu_field_names_mapping = {"in_port": "in_port",
                           "eth_type": "ethernet_type",
                           "eth_src": "ethernet_source",
                           "eth_dst": "ethernet_destination",
                           "nw_src": "src_ip_addr",
                           "nw_dst": "dst_ip_addr",
                           "ip_proto": "ip_protocol",
                           "tcp_dst": "tcp_destination_port",
                           "tcp_src": "tcp_source_port",
                           "udp_dst": "udp_destination_port",
                           "udp_src": "udp_source_port",
                           "vlan_vid": "vlan_id"}

ryu_field_names_mapping_reverse = {"in_port": "in_port",
                                   "ethernet_type": "eth_type",
                                   "ethernet_source": "eth_src",
                                   "ethernet_destination": "eth_dst",
                                   "src_ip_addr": "nw_src",
                                   "dst_ip_addr": "nw_dst",
                                   "ip_protocol": "nw_proto",
                                   "tcp_destination_port": "tcp_dst",
                                   "tcp_source_port": "tcp_src",
                                   "udp_destination_port": "udp_dst",
                                   "udp_source_port": "udp_src",
                                   "vlan_id": "vlan_vid"}


class OdlMatchJsonParser:

    def __init__(self, match_json=None):
        self.field_values = {}
        self._parse(match_json)

    def _parse(self, match_json):

        for field_name in field_names:

            try:
                if field_name == "in_port":
                     self[field_name] = match_json["in-port"]

                elif field_name == "ethernet_type":
                    self[field_name] = match_json["ethernet-match"]["ethernet-type"]["type"]

                elif field_name == "ethernet_source":
                     self[field_name] = match_json["ethernet-match"]["ethernet-source"]["address"]

                elif field_name == "ethernet_destination":
                    self[field_name] = match_json["ethernet-match"]["ethernet-destination"]["address"]

                elif field_name == "src_ip_addr":
                    self[field_name] =  match_json["src_ip_addr"]

                elif field_name == "dst_ip_addr":
                    self[field_name] =  match_json["dst_ip_addr"]

                elif field_name == "ip_protocol":
                    self[field_name] = match_json["ip-match"]["ip-protocol"]

                elif field_name == "tcp_destination_port":
                    self[field_name] = match_json["tcp-destination-port"]

                elif field_name == "tcp_source_port":
                    self[field_name] = match_json["tcp-source-port"]

                elif field_name == "udp_destination_port":
                    self[field_name] = match_json["udp-destination-port"]

                elif field_name == "udp_source_port":
                    self[field_name] = match_json["udp-source-port"]

                elif field_name == "vlan_id":
                    self[field_name] = match_json["vlan-match"]["vlan-id"]["vlan-id"]

            except KeyError:
                continue

    def __getitem__(self, item):
        return self.field_values[item]

    def __setitem__(self, field_name, value):
        self.field_values[field_name] = value

    def __delitem__(self, field_name):
        del self.field_values[field_name]

    def keys(self):
        return self.field_values.keys()

class Match(DictMixin):

    def __getitem__(self, item):
        return self.match_field_values[item]

    def __setitem__(self, key, value):
        self.match_field_values[key] = value

    def __delitem__(self, key):
        del self.match_field_values[key]

    def keys(self):
        return self.match_field_values.keys()

    def __init__(self, match_json=None, controller=None, flow=None, is_wildcard=True):

        self.flow = flow
        self.match_field_values = {}

        if match_json and controller == "odl":
            raise NotImplemented
        elif match_json and controller == "ryu":
            self.add_element_from_ryu_match_json(match_json)
        elif match_json and controller == "sel":
            raise NotImplemented
        elif is_wildcard:
            for field_name in field_names:
                self.match_field_values[field_name] = sys.maxsize

    def is_match_field_wildcard(self, field_name):
        return self.match_field_values[field_name] == sys.maxsize

    def add_element_from_odl_match_json(self, match_json):

        for field_name in field_names:
            try:
                if field_name == "in_port":
                    try:
                        self[field_name] = int(match_json["in-port"])
                    except ValueError:
                        parsed_in_port = match_json["in-port"].split(":")[2]
                        self[field_name] = int(parsed_in_port)

                elif field_name == "ethernet_type":
                    self[field_name] = int(match_json["ethernet-match"]["ethernet-type"]["type"])
                elif field_name == "ethernet_source":
                    mac_int = int(match_json["ethernet-match"]["ethernet-source"]["address"].replace(":", ""), 16)
                    self[field_name] = mac_int

                elif field_name == "ethernet_destination":
                    mac_int = int(match_json["ethernet-match"]["ethernet-destination"]["address"].replace(":", ""), 16)
                    self[field_name] = mac_int

                #TODO: Add graceful handling of IP addresses
                elif field_name == "src_ip_addr":
                    self[field_name] = IPNetwork(match_json["src_ip_addr"])
                elif field_name == "dst_ip_addr":
                    self[field_name] = IPNetwork(match_json["dst_ip_addr"])

                elif field_name == "ip_protocol":
                    self[field_name] = int(match_json["ip-match"]["ip-protocol"])
                elif field_name == "tcp_destination_port":
                    self[field_name] = int(match_json["tcp-destination-port"])
                elif field_name == "tcp_source_port":
                    self[field_name] = int(match_json["tcp-source-port"])
                elif field_name == "udp_destination_port":
                    self[field_name] = int(match_json["udp-destination-port"])
                elif field_name == "udp_source_port":
                    self[field_name] = int(match_json["udp-source-port"])
                elif field_name == "vlan_id":
                    self[field_name] = int(match_json["vlan-match"]["vlan-id"]["vlan-id"])

            except KeyError:
                self[field_name] = sys.maxsize
                continue

    def add_element_from_ryu_match_json(self, match_json):

        for field_name in field_names:

            try:
                if field_name == "in_port":
                    try:
                        self[field_name] = int(match_json["in_port"])

                    except ValueError:
                        parsed_in_port = match_json["in-port"].split(":")[2]
                        self[field_name] = int(parsed_in_port)

                elif field_name == "ethernet_type":
                    self[field_name] = int(match_json["eth_type"])

                elif field_name == "ethernet_source":
                    mac_int = int(match_json[u"eth_src"].replace(":", ""), 16)
                    self[field_name] = mac_int

                elif field_name == "ethernet_destination":
                    mac_int = int(match_json[u"eth_dst"].replace(":", ""), 16)
                    self[field_name] = mac_int

                #TODO: Add graceful handling of IP addresses
                elif field_name == "src_ip_addr":
                    self[field_name] = IPNetwork(match_json["nw_src"])
                elif field_name == "dst_ip_addr":
                    self[field_name] = IPNetwork(match_json["nw_dst"])

                elif field_name == "ip_protocol":
                    self[field_name] = int(match_json["nw_proto"])
                elif field_name == "tcp_destination_port":

                    if match_json["nw_proto"] == 6:
                        self[field_name] = int(match_json["tp_dst"])
                    else:
                        self[field_name] = match_json["zzzz"]

                elif field_name == "tcp_source_port":

                     if match_json["nw_proto"] == 6:
                        self[field_name] = int(match_json["tp_src"])
                     else:
                        self[field_name] = match_json["zzzz"]

                elif field_name == "udp_destination_port":

                    if match_json["nw_proto"] == 17:
                        self[field_name] = int(match_json["tp_dst"])
                    else:
                        self[field_name] = match_json["zzzz"]

                elif field_name == "udp_source_port":

                     if match_json["nw_proto"] == 17:
                        self[field_name] = int(match_json["tp_src"])
                     else:
                        self[field_name] = match_json["zzzz"]

                elif field_name == "vlan_id":

                    if match_json[u"vlan_vid"] == "0x1000/0x1000":
                        self[field_name] = sys.maxsize
                        self["has_vlan_tag"] = 1
                    else:
                        self[field_name] = 0x1000 + int(match_json[u"vlan_vid"])
                        self["has_vlan_tag"] = 1

            except KeyError:
                self[field_name] = sys.maxsize

                if field_name == 'vlan_id':
                    self["has_vlan_tag"] = sys.maxsize

                continue

    def generate_ryu_match_json(self, match_json, has_vlan_tag_check=False):

        for field_name in field_names:

            if has_vlan_tag_check:
                if field_name == "vlan_id":
                    match_json[ryu_field_names_mapping_reverse[field_name]] = "0x1000/0x1000"

            if field_name in self and self[field_name] != sys.maxsize:

                if field_name == "ethernet_source" or field_name == "ethernet_destination":

                    #print "self[field_name]:", self[field_name]
                    mac_hex_str = hex(self[field_name])[2:]
                    #print "mac_hex_str:", mac_hex_str
                    if len(mac_hex_str) == 11:
                        mac_hex_str = "0" + mac_hex_str

                    mac_hex_str = unicode(':'.join(s.encode('hex') for s in mac_hex_str.decode('hex')))
                    match_json[ryu_field_names_mapping_reverse[field_name]] = mac_hex_str
                else:
                    match_json[ryu_field_names_mapping_reverse[field_name]] = self[field_name]

        return match_json

    def generate_match_json(self, controller, match_json, has_vlan_tag_check=False):

        if controller == "ryu":
            return self.generate_ryu_match_json(match_json, has_vlan_tag_check)
        elif controller == "ryu_old":
            return self.generate_ryu_match_json(match_json, has_vlan_tag_check)
        else:
            raise NotImplementedError
