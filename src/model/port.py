__author__ = 'Rakesh Kumar'


class Port(object):

    def __init__(self, sw, port_json):

        self.sw = sw
        self.port_id = None
        self.curr_speed = None
        self.max_speed = None

        self.mac_address = None
        self.port_number = None
        self.state = None
        self.attached_host = None

        if self.sw.network_graph.controller == "ryu":
            self.parse_ryu_port_json(port_json)
        elif self.sw.network_graph.controller == "ryu_old":
            self.parse_ryu_port_json(port_json)
        else:
            raise NotImplemented

    def parse_ryu_port_json(self, port_json):

        self.port_id = str(self.sw.node_id) + ":" + str(port_json["port_no"])
        self.port_number = port_json["port_no"]
        self.mac_address = port_json["hw_addr"]

        if "curr_speed" in port_json:
            self.curr_speed = int(port_json["curr_speed"])
        if "max_speed" in port_json:
            self.max_speed = int(port_json["max_speed"])

        #TODO: Peep into port_json["state"]
        self.state = "up"

    def __str__(self):
        return str(self.port_id)
