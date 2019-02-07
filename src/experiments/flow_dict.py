
all_flows = [
    {"id": "f1", "type": "data", "port": 10000, "client": "dot08", "server": "dot09", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority":6
     #,"path": ["dot08", "ps3", "ps4", "dot09"]
     ,"path": ["dot08", "ps3", "ps2", "ps4", "dot09"]
     #,"path": ["dot08", "ps3", "ps1", "ps1", "ps4", "dot09"]
     },
    {"id": "f2", "type": "data", "port": 10001, "client": "dot10", "server": "dot11", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot10", "ps3", "ps4", "dot11"]
     #,"path": ["dot10", "ps3", "ps2", "ps4", "dot11"]
     #,"path": ["dot10", "ps3", "ps1", "ps2", "ps4", "dot11"]
     },
    {"id": "f3", "type": "data", "port": 10002, "client": "dot12", "server": "dot15", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot12", "ps3", "ps4", "dot15"]
     #,"path": ["dot12", "ps3", "ps2", "ps4", "dot15"]
     #,"path": ["dot12", "ps3", "ps1", "ps2", "ps4", "dot15"]
     },
    {"id": "f4", "type": "data", "port": 10003, "client": "dot20", "server": "dot29", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot20", "ps3", "ps4", "dot29"]
     #,"path": ["dot20", "ps3", "ps2", "ps4", "dot29"]
     #,"path": ["dot20", "ps3", "ps1", "ps2", "ps4", "dot29"]
     },

    # {"id": "f5", "type": "data", "port": 10004, "client": "dot30", "server": "dot31", "rate":95,
    #  "data_loc": "/home/pi/", "user": "pi", "priority": 6
    #  ,"path": ["dot30", "ps3", "ps4", "dot31"]
    #  #,"path": ["dot30", "ps3", "ps2", "ps4", "dot31"]
    #  #,"path": ["dot30", "ps3", "ps1", "ps2", "ps4", "dot31"]
    #  },

    {"id": "f6", "type": "data", "port": 10005, "client": "dot40", "server": "dot120", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot40", "ps3", "ps4", "dot120"]
     #,"path": ["dot40", "ps3", "ps2", "ps4", "dot120"]
     #,"path": ["dot40", "ps3", "ps1", "ps2", "ps4", "dot120"]
     },

    {"id": "f7", "type": "data", "port": 10006, "client": "dot50", "server": "dot60", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot50", "ps3", "ps4", "dot60"]
     #,"path": ["dot50", "ps3", "ps2", "ps4", "dot60"]
     #,"path": ["dot50", "ps3", "ps1", "ps2", "ps4", "dot60"]
     },

    {"id": "f8", "type": "data", "port": 10007, "client": "dot70", "server": "dot80", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot70", "ps3", "ps4", "dot80"]
     #,"path": ["dot70", "ps3", "ps2", "ps4", "dot80"]
     #,"path": ["dot70", "ps3", "ps1", "ps2", "ps4", "dot80"]
     },

    {"id": "f9", "type": "data", "port": 10008, "client": "dot140", "server": "dot200", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot140", "ps3", "ps4", "dot200"]
     #,"path": ["dot140", "ps3", "ps2", "ps4", "dot200"]
     #,"path": ["dot140", "ps3", "ps1", "ps2", "ps4", "dot200"]
     },

    {"id": "f10", "type": "data", "port": 10009, "client": "dot220", "server": "dot240", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot220", "ps3", "ps4", "dot240"]
     #,"path": ["dot220", "ps3", "ps2", "ps4", "dot240"]
     #,"path": ["dot220", "ps3", "ps1", "ps2", "ps4", "dot240"]
     },

    {"id": "f11", "type": "data", "port": 10010, "client": "dot242", "server": "dot244", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
      ,"path": ["dot242", "ps3", "ps4", "dot244"]
     # ,"path": ["dot242", "ps3", "ps2", "ps4", "dot244"]
     # ,"path": ["dot242", "ps3", "ps1", "ps2", "ps4", "dot244"]
     },

    {"id": "f12", "type": "data", "port": 10011, "client": "dot245", "server": "dot246", "rate":95,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
      ,"path": ["dot245", "ps3", "ps4", "dot246"]
      #,"path": ["dot245", "ps3", "ps2", "ps4", "dot246"]
     # ,"path": ["dot245", "ps3", "ps1", "ps2", "ps4", "dot246"]
     },

    # {"id": "f13", "type": "data", "port": 10012, "client": "dot247", "server": "dot248", "rate": 90,
    #  "data_loc": "/home/pi/", "user": "pi", "priority": 6
    #  #,"path": ["dot247", "ps3", "ps4", "dot248"]
    #  ,"path": ["dot247", "ps3", "ps2", "ps4", "dot248"]
    #  # ,"path": ["dot247", "ps3", "ps1", "ps2", "ps4", "dot249"]
    #  },

    # {"id": "flaptop", "type": "data", "port": 10013, "client": "dot250", "server": "dot123", "rate": 5,
    #  "data_loc": "/home/iti/", "user": "iti", "priority": 1
    #  ,"path": ["dot250", "ps1", "ps2", "ps3", "ps4", "dot123"]
    #  },


    # Time Synchronization Flows
    # This has to be auto-generated in the future


    {"id": "ptp_1_f1", "type": "ptp", "port": 319, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot08", "ps3", "ps1", "ps2", "ps4", "dot09"]
     },
    {"id": "ptp_2_f1", "type": "ptp", "port": 320, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot08", "ps3", "ps1", "ps2", "ps4", "dot09"]
     },
    {"id": "ptp_3_f1", "type": "ptp", "port": 319, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot09", "ps4", "ps2", "ps1", "ps3", "dot08"]
     },
    {"id": "ptp_4_f1", "type": "ptp", "port": 320, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot09", "ps4", "ps2", "ps1", "ps3", "dot08"]
     },

    {"id": "ptp_1_f2", "type": "ptp", "port": 319, "client": "dot10", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot10", "ps3", "ps1", "ps2", "ps4", "dot11"]
     },
    {"id": "ptp_2_f2", "type": "ptp", "port": 320, "client": "dot10", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot10", "ps3", "ps1", "ps2", "ps4", "dot11"]
     },
    {"id": "ptp_3_f2", "type": "ptp", "port": 319, "client": "dot11", "server": "dot10", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot11", "ps4", "ps2", "ps1", "ps3", "dot10"]
     },
    {"id": "ptp_4_f2", "type": "ptp", "port": 320, "client": "dot11", "server": "dot10", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot11", "ps4", "ps2", "ps1", "ps3", "dot10"]
     },

    {"id": "ptp_1_f3", "type": "ptp", "port": 319, "client": "dot12", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot12", "ps3", "ps1", "ps2", "ps4", "dot15"]
     },
    {"id": "ptp_2_f3", "type": "ptp", "port": 320, "client": "dot12", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot12", "ps3", "ps1", "ps2", "ps4", "dot15"]
     },
    {"id": "ptp_3_f3", "type": "ptp", "port": 319, "client": "dot15", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot15", "ps4", "ps2", "ps1", "ps3", "dot12"]
     },
    {"id": "ptp_4_f3", "type": "ptp", "port": 320, "client": "dot15", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot15", "ps4", "ps2", "ps1", "ps3", "dot12"]
     },
    
     {"id": "ptp_1_f4", "type": "ptp", "port": 319, "client": "dot20", "server": "dot29", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot20", "ps3", "ps1", "ps2", "ps4", "dot29"]
     },
    {"id": "ptp_2_f4", "type": "ptp", "port": 320, "client": "dot20", "server": "dot29", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot20", "ps3", "ps1", "ps2", "ps4", "dot29"]
     },
    {"id": "ptp_3_f4", "type": "ptp", "port": 319, "client": "dot29", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot29", "ps4", "ps2", "ps1", "ps3", "dot20"]
     },
    {"id": "ptp_4_f4", "type": "ptp", "port": 320, "client": "dot29", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot29", "ps4", "ps2", "ps1", "ps3", "dot20"]
     },    
    
    {"id": "ptp_1_f5", "type": "ptp", "port": 319, "client": "dot30", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot30", "ps3", "ps1", "ps2", "ps4", "dot31"]
     },
    {"id": "ptp_2_f5", "type": "ptp", "port": 320, "client": "dot30", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot30", "ps3", "ps1", "ps2", "ps4", "dot31"]
     },
    {"id": "ptp_3_f5", "type": "ptp", "port": 319, "client": "dot31", "server": "dot30", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot31", "ps4", "ps2", "ps1", "ps3", "dot30"]
     },
    {"id": "ptp_4_f5", "type": "ptp", "port": 320, "client": "dot31", "server": "dot30", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot31", "ps4", "ps2", "ps1", "ps3", "dot30"]
     },

    {"id": "ptp_1_f6", "type": "ptp", "port": 319, "client": "dot40", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot40", "ps3", "ps1", "ps2","ps4", "dot120"]
     },
    {"id": "ptp_2_f6", "type": "ptp", "port": 320, "client": "dot40", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot40", "ps3", "ps1", "ps2","ps4", "dot120"]
     },
    {"id": "ptp_3_f6", "type": "ptp", "port": 319, "client": "dot120", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot120", "ps4", "ps2", "ps1","ps3", "dot40"]
     },
    {"id": "ptp_4_f6", "type": "ptp", "port": 320, "client": "dot120", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot120", "ps4", "ps2", "ps1","ps3", "dot40"]
     },

    {"id": "ptp_1_f7", "type": "ptp", "port": 319, "client": "dot50", "server": "dot60", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot50", "ps3", "ps1", "ps2", "ps4", "dot60"]
     },
    {"id": "ptp_2_f7", "type": "ptp", "port": 320, "client": "dot50", "server": "dot60", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot50", "ps3", "ps1", "ps2", "ps4", "dot60"]
     },
    {"id": "ptp_3_f7", "type": "ptp", "port": 319, "client": "dot60", "server": "dot50", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot60", "ps4", "ps2", "ps1", "ps3", "dot50"]
     },
    {"id": "ptp_4_f7", "type": "ptp", "port": 320, "client": "dot60", "server": "dot50", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot60", "ps4", "ps2", "ps1", "ps3", "dot50"]
     },

    {"id": "ptp_1_f8", "type": "ptp", "port": 319, "client": "dot70", "server": "dot80", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot70", "ps3", "ps1", "ps2", "ps4", "dot80"]
     },
    {"id": "ptp_2_f8", "type": "ptp", "port": 320, "client": "dot70", "server": "dot80", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot70", "ps3", "ps1", "ps2", "ps4", "dot80"]
     },
    {"id": "ptp_3_f8", "type": "ptp", "port": 319, "client": "dot80", "server": "dot70", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot80", "ps4", "ps2", "ps1", "ps3", "dot70"]
     },
    {"id": "ptp_4_f8", "type": "ptp", "port": 320, "client": "dot80", "server": "dot70", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot80", "ps4", "ps2", "ps1", "ps3", "dot70"]
     },
    
    

    {"id": "ptp_1_f9", "type": "ptp", "port": 319, "client": "dot140", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot140", "ps3","ps1", "ps2", "ps4", "dot200"]
     },
    {"id": "ptp_2_f9", "type": "ptp", "port": 320, "client": "dot140", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot140", "ps3", "ps1", "ps2", "ps4", "dot200"]
     },
    {"id": "ptp_3_f9", "type": "ptp", "port": 319, "client": "dot200", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot200", "ps4", "ps2", "ps1", "ps3", "dot140"]
     },
    {"id": "ptp_4_f9", "type": "ptp", "port": 320, "client": "dot200", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot200", "ps4", "ps2", "ps1", "ps3", "dot140"]
     },

    {"id": "ptp_1_f10", "type": "ptp", "port": 319, "client": "dot220", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot220", "ps3","ps1", "ps2", "ps4", "dot240"]
     },
    {"id": "ptp_2_f10", "type": "ptp", "port": 320, "client": "dot220", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot220", "ps3","ps1", "ps2", "ps4", "dot240"]
     },
    {"id": "ptp_3_f10", "type": "ptp", "port": 319, "client": "dot240", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot240", "ps4", "ps2", "ps1", "ps3", "dot220"]
     },
    {"id": "ptp_4_f10", "type": "ptp", "port": 320, "client": "dot240", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot240", "ps4", "ps2", "ps1", "ps3", "dot220"]
     },

    {"id": "ptp_1_f11", "type": "ptp", "port": 319, "client": "dot242", "server": "dot244", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot242", "ps3","ps1", "ps2", "ps4", "dot244"]
     },
    {"id": "ptp_2_f11", "type": "ptp", "port": 320, "client": "dot242", "server": "dot244", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot242", "ps3","ps1", "ps2", "ps4", "dot244"]
     },
    {"id": "ptp_3_f11", "type": "ptp", "port": 319, "client": "dot244", "server": "dot242", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot244", "ps4", "ps2", "ps1", "ps3", "dot242"]
     },
    {"id": "ptp_4_f11", "type": "ptp", "port": 320, "client": "dot244", "server": "dot242", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot244", "ps4", "ps2", "ps1", "ps3", "dot242"]
     },

    {"id": "ptp_1_f12", "type": "ptp", "port": 319, "client": "dot245", "server": "dot246", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot245", "ps3","ps1", "ps2", "ps4", "dot246"]
     },
    {"id": "ptp_2_f12", "type": "ptp", "port": 320, "client": "dot245", "server": "dot246", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot245", "ps3","ps1", "ps2", "ps4", "dot246"]
     },
    {"id": "ptp_3_f12", "type": "ptp", "port": 319, "client": "dot246", "server": "dot245", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot246", "ps4", "ps2", "ps1", "ps3", "dot245"]
     },
    {"id": "ptp_4_f12", "type": "ptp", "port": 320, "client": "dot246", "server": "dot245", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot246", "ps4", "ps2", "ps1", "ps3", "dot245"]
     },

    {"id": "ptp_1_f13", "type": "ptp", "port": 319, "client": "dot247", "server": "dot248", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot247", "ps3","ps1", "ps2", "ps4", "dot248"]
     },
    {"id": "ptp_2_f13", "type": "ptp", "port": 320, "client": "dot247", "server": "dot248", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot247", "ps3","ps1", "ps2", "ps4", "dot248"]
     },
    {"id": "ptp_3_f13", "type": "ptp", "port": 319, "client": "dot248", "server": "dot247", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot248", "ps4", "ps2", "ps1", "ps3", "dot247"]
     },
    {"id": "ptp_4_f13", "type": "ptp", "port": 320, "client": "dot248", "server": "dot247", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot248", "ps4", "ps2", "ps1", "ps3", "dot247"]
     },

    {"id": "ptp_1_f14", "type": "ptp", "port": 319, "client": "dot250", "server": "dot123", "rate": 50,
     "data_loc": "/home/iti/", "user": "iti", "priority": 7,
     "path": ["dot250", "ps1","ps2", "ps3", "ps4", "dot123"]
     },
    {"id": "ptp_2_f14", "type": "ptp", "port": 320, "client": "dot250", "server": "dot123", "rate": 50,
     "data_loc": "/home/iti/", "user": "iti", "priority": 7,
    "path": ["dot250", "ps1","ps2", "ps3", "ps4", "dot123"]
     },
    {"id": "ptp_3_f14", "type": "ptp", "port": 319, "client": "dot123", "server": "dot250", "rate": 50,
     "data_loc": "/home/iti/", "user": "iti", "priority": 7,
     "path": ["dot123", "ps4","ps3", "ps2", "ps1", "dot250"]
     },
    {"id": "ptp_4_f14", "type": "ptp", "port": 320, "client": "dot123", "server": "dot250", "rate": 50,
     "data_loc": "/home/iti/", "user": "iti", "priority": 7,
     "path": ["dot123", "ps4","ps3", "ps2", "ps1", "dot250"]
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





