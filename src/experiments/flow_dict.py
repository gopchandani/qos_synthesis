

all_flows = [
    {"id": "f1", "port": 10000, "client": "dot08", "server": "dot09", "rate": 10,
     "data_loc": "/home/pi/", "user": "pi",
     "rules":
         [
             {"sw_name": "ps1", "flow_type":"normal", "out_port": "ge-1/1/2", "src_ip": "192.168.1.8", "dst_ip": "192.168.1.9",
              "queue_num": 3, "flow_rule_priority": 2},
             {"sw_name": "ps2", "flow_type":"normal", "out_port": "ge-1/1/6", "src_ip": "192.168.1.8", "dst_ip": "192.168.1.9",
              "queue_num": 3, "flow_rule_priority": 2},
             {"sw_name": "ps4", "flow_type":"normal", "out_port": "ge-1/1/1", "src_ip": "192.168.1.8", "dst_ip": "192.168.1.9",
              "queue_num": 3, "flow_rule_priority": 2},
             {"sw_name": "ps2", "flow_type":"group", "group_id": 1, "src_ip": "192.168.1.8", "dst_ip": "192.168.1.9", "flow_rule_priority": 99},
         ],
     "queues":
         [
             {"sw_name": "ps1", "out_port": "ge-1/1/2", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3},
             {"sw_name": "ps2", "out_port": "ge-1/1/4", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3},
             {"sw_name": "ps2", "out_port": "ge-1/1/6", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3},
             {"sw_name": "ps3", "out_port": "ge-1/1/10", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3},
             {"sw_name": "ps4", "out_port": "ge-1/1/1", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3}
         ],

     "groups":[

            {"sw_name":"ps2", "group_id":1, "group_type":"fast_failover", "buckets":[{"watch_port":"ge-1/1/6",
                                                                                    "output_port":"ge-1/1/6"
                                                                                    },
                                                                                   {"watch_port":"ge-1/1/4",
                                                                                    "output_port":"ge-1/1/4"
                                                                                   }]
             }

         ]
     },



]

    # {"id": "f2", "port": 10001, "client": "dot10", "server": "dot11", "rate": 50,
    #  "data_loc": "/home/pi/", "user": "pi"},
    # {"id": "f3", "port": 10002, "client": "dot12", "server": "dot15", "rate": 50,
    #  "data_loc": "/home/pi/", "user": "pi"},
    # {"id": "f4", "port": 10003, "client": "dot20", "server": "dot29", "rate": 50,
    #  "data_loc": "/home/pi/", "user": "pi"},
    # {"id": "f5", "port": 10004, "client": "dot30", "server": "dot31", "rate": 50,
    #  "data_loc": "/home/pi/", "user": "pi"},
    # {"id": "f6", "port": 10005, "client": "dot40", "server": "dot120", "rate": 50,
    #  "data_loc": "/home/pi/", "user": "pi"},
    # {"id": "f7", "port": 10006, "client": "dot140", "server": "dot200", "rate": 50,
    #  "data_loc": "/home/pi/", "user": "pi"},
    # {"id": "f8", "port": 10007, "client": "dot220", "server": "dot240", "rate": 50,
    #  "data_loc": "/home/pi/", "user": "pi"}


# all_flows = [
#     {"id": "f1", "port": 10000, "client": "dot08", "server": "dot09", "rate": 30,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f2", "port": 10001, "client": "dot10", "server": "dot11", "rate": 30,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f3", "port": 10002, "client": "dot12", "server": "dot15", "rate": 30,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f4", "port": 10003, "client": "dot20", "server": "dot29", "rate": 30,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f5", "port": 10004, "client": "dot30", "server": "dot31", "rate": 30,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f6", "port": 10005, "client": "dot40", "server": "dot120", "rate": 30,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f7", "port": 10006, "client": "dot140", "server": "dot200", "rate": 30,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f8", "port": 10007, "client": "dot220", "server": "dot240", "rate": 30,
#      "data_loc": "/home/pi/", "user": "pi"}
# ]

# all_flows = [
#     {"id": "f1", "port": 10000, "client": "dot08", "server": "dot09", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f2", "port": 10001, "client": "dot10", "server": "dot11", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f3", "port": 10002, "client": "dot12", "server": "dot15", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f4", "port": 10003, "client": "dot20", "server": "dot29", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f5", "port": 10004, "client": "dot30", "server": "dot31", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f6", "port": 10005, "client": "dot40", "server": "dot120", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f7", "port": 10006, "client": "dot140", "server": "dot200", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi"},
#     {"id": "f8", "port": 10007, "client": "dot220", "server": "dot240", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi"}
# ]

flow_f1 = [
    {"id": "f1", "port": 10000, "client": "dot08", "server": "dot09", "rate": 10,
     "data_loc": "/home/pi/", "user": "pi"}
]

flow_f2 = [
    {"id": "f2", "port": 10001, "client": "dot10", "server": "dot11", "rate": 3,
     "data_loc": "/home/pi/", "user": "pi"}
]

flow_f3 = [
    {"id": "f3", "port": 10002, "client": "dot12", "server": "dot15", "rate": 3,
     "data_loc": "/home/pi/", "user": "pi"}
]

flow_f4 = [
    {"id": "f4", "port": 10003, "client": "dot20", "server": "dot29", "rate": 3,
     "data_loc": "/home/pi/", "user": "pi"}
]


flow_f5 = [
    {"id": "f5", "port": 10004, "client": "dot30", "server": "dot31", "rate": 3,
     "data_loc": "/home/pi/", "user": "pi"}
]

flow_f6 = [
    {"id": "f6", "port": 10005, "client": "dot40", "server": "dot120", "rate": 3,
     "data_loc": "/home/pi/", "user": "pi"}
]

flow_f7 = [
    {"id": "f7", "port": 10006, "client": "dot140", "server": "dot200", "rate": 3,
     "data_loc": "/home/pi/", "user": "pi"}
]

flow_f8 = [
    {"id": "f8", "port": 10007, "client": "dot220", "server": "dot240", "rate": 3,
     "data_loc": "/home/pi/", "user": "pi"}
]


flow_f8 = [
    {"id": "f8", "port": 10100, "client": "dot220", "server": "dot240", "rate": 50,
     "data_loc": "/home/iti/", "user": "iti"}
]
