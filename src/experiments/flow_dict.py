
all_flows = [
    {"id": "f1", "type": "data", "port": 10000, "client": "dot08", "server": "dot09", "rate": 60,
     "data_loc": "/home/pi/", "user": "pi", "priority":6
     ,"path": ["dot08", "ps1", "ps4", "dot09"]
     #,"path": ["dot08", "ps1", "ps2", "ps4", "dot09"]
     #,"path": ["dot08", "ps1", "ps2", "ps3", "ps4", "dot09"]

        },
    {"id": "f2", "type": "data", "port": 10001, "client": "dot10", "server": "dot11", "rate": 60,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     ,"path": ["dot10", "ps1", "ps4", "dot11"]
     #,"path": ["dot10", "ps1", "ps2", "ps4", "dot11"]
     #,"path": ["dot10", "ps1", "ps2", "ps3", "ps4", "dot11"]
     },
    {"id": "f3", "type": "data", "port": 10002, "client": "dot12", "server": "dot15", "rate": 60,
     "data_loc": "/home/pi/", "user": "pi", "priority": 4
     ,"path": ["dot12", "ps1", "ps4", "dot15"]
     #,"path": ["dot12", "ps1", "ps2", "ps4", "dot15"]
     #,"path": ["dot12", "ps1", "ps2", "ps3", "ps4", "dot15"]
     },
    {"id": "f4", "type": "data", "port": 10003, "client": "dot20", "server": "dot29", "rate": 60,
     "data_loc": "/home/pi/", "user": "pi", "priority": 3
     ,"path": ["dot20", "ps1", "ps4", "dot29"]
     #,"path": ["dot20", "ps1", "ps2", "ps4", "dot29"]
     #,"path": ["dot20", "ps1", "ps2", "ps3", "ps4", "dot29"]
     },
    {"id": "f5", "type": "data", "port": 10004, "client": "dot30", "server": "dot31", "rate": 60,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot30", "ps2", "ps4", "dot31"]
     #,"path": ["dot30", "ps2", "ps3", "ps4", "dot31"]
     },
    {"id": "f6", "type": "data", "port": 10005, "client": "dot40", "server": "dot120", "rate": 60,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     ,"path": ["dot40", "ps2", "ps4", "dot120"]
     #,"path": ["dot40", "ps2", "ps3", "ps4", "dot120"]
     },
    {"id": "f7", "type": "data", "port": 10006, "client": "dot140", "server": "dot200", "rate": 60,
     "data_loc": "/home/pi/", "user": "pi", "priority": 4
     ,"path": ["dot140", "ps2", "ps4", "dot200"]
     #,"path": ["dot140", "ps2", "ps3", "ps4", "dot200"]
     },
    {"id": "f8", "type": "data", "port": 10007, "client": "dot220", "server": "dot240", "rate": 60,
     "data_loc": "/home/pi/", "user": "pi", "priority": 3
     ,"path": ["dot220", "ps2", "ps4", "dot240"]
     #,"path": ["dot220", "ps2", "ps3", "ps4", "dot240"]
     },
    {"id": "f_background", "type": "bg", "port": 10008, "client": "dot250", "server": "dot123", "rate": 800,
     "data_loc": "/home/iti/", "user": "iti", "priority": 3
     ,"path": ["dot250", "ps2", "ps4", "dot123"]
     },
    {"id": "f_background_2", "type": "bg", "port": 10009, "client": "dot102", "server": "dot123", "rate": 800,
     "data_loc": "/home/iti/", "user": "iti", "priority": 3
     ,"path": ["dot102", "ps1", "ps4", "dot123"]
     },


    {"id": "ptp_1_f1", "type": "ptp", "port": 319, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f1", "type": "ptp", "port": 320, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f1", "type": "ptp", "port": 319, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f1", "type": "ptp", "port": 320, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f2", "type": "ptp", "port": 319, "client": "dot10", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f2", "type": "ptp", "port": 320, "client": "dot10", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f2", "type": "ptp", "port": 319, "client": "dot11", "server": "dot10", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f2", "type": "ptp", "port": 320, "client": "dot11", "server": "dot10", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f3", "type": "ptp", "port": 319, "client": "dot12", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f3", "type": "ptp", "port": 320, "client": "dot12", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f3", "type": "ptp", "port": 319, "client": "dot15", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f3", "type": "ptp", "port": 320, "client": "dot15", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f4", "type": "ptp", "port": 319, "client": "dot20", "server": "dot29", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f4", "type": "ptp", "port": 320, "client": "dot20", "server": "dot29", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f4", "type": "ptp", "port": 319, "client": "dot29", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f4", "type": "ptp", "port": 320, "client": "dot29", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f5", "type": "ptp", "port": 319, "client": "dot30", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f5", "type": "ptp", "port": 320, "client": "dot30", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f5", "type": "ptp", "port": 319, "client": "dot31", "server": "dot30", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f5", "type": "ptp", "port": 320, "client": "dot31", "server": "dot30", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f6", "type": "ptp", "port": 319, "client": "dot40", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f6", "type": "ptp", "port": 320, "client": "dot40", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f6", "type": "ptp", "port": 319, "client": "dot120", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f6", "type": "ptp", "port": 320, "client": "dot120", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f7", "type": "ptp", "port": 319, "client": "dot140", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f7", "type": "ptp", "port": 320, "client": "dot140", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f7", "type": "ptp", "port": 319, "client": "dot200", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f7", "type": "ptp", "port": 320, "client": "dot200", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f8", "type": "ptp", "port": 319, "client": "dot220", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f8", "type": "ptp", "port": 320, "client": "dot220", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f8", "type": "ptp", "port": 319, "client": "dot240", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f8", "type": "ptp", "port": 320, "client": "dot240", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
]



# all_flows = [
#     {"id": "f1", "port": 10000, "client": "dot08", "server": "dot09", "rate": 10,
#      "data_loc": "/home/pi/", "user": "pi",
#      "rules":
#          [
#              {"sw_name": "ps1", "flow_type":"normal", "out_port": "ge-1/1/2", "src_ip": "192.168.1.8", "dst_ip": "192.168.1.9",
#               "queue_num": 3, "flow_rule_priority": 2},
#              {"sw_name": "ps2", "flow_type":"normal", "out_port": "ge-1/1/6", "src_ip": "192.168.1.8", "dst_ip": "192.168.1.9",
#               "queue_num": 3, "flow_rule_priority": 2},
#              {"sw_name": "ps4", "flow_type":"normal", "out_port": "ge-1/1/1", "src_ip": "192.168.1.8", "dst_ip": "192.168.1.9",
#               "queue_num": 3, "flow_rule_priority": 2},
#              {"sw_name": "ps2", "flow_type":"group", "group_id": 1, "src_ip": "192.168.1.8", "dst_ip": "192.168.1.9", "flow_rule_priority": 99},
#          ],
#      "queues":
#          [
#              {"sw_name": "ps1", "out_port": "ge-1/1/2", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3},
#              {"sw_name": "ps2", "out_port": "ge-1/1/4", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3},
#              {"sw_name": "ps2", "out_port": "ge-1/1/6", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3},
#              {"sw_name": "ps3", "out_port": "ge-1/1/10", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3},
#              {"sw_name": "ps4", "out_port": "ge-1/1/1", "min_rate": 1000000000, "max_rate": 1000000000, "queue_priority": 3}
#          ],
#
#      "groups":[
#
#             {"sw_name":"ps2", "group_id":1, "group_type":"fast_failover", "buckets":[{"watch_port":"ge-1/1/6",
#                                                                                     "output_port":"ge-1/1/6"
#                                                                                     },
#                                                                                    {"watch_port":"ge-1/1/4",
#                                                                                     "output_port":"ge-1/1/4"
#                                                                                    }]
#              }
#
#          ]
#      },
#
#
#
# ]

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
    {"id": "f8", "port": 10008, "client": "dot220", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi"}
]
