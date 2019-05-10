
all_flows = [
    # FLIGHT CONTROL
    {"id": "f1", "type": "data", "port": 10000, "client": "dot08", "server": "dot09", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority":4
     ,"path": ["dot08", "ps2", "ps4", "dot09"]
     #,"path": ["dot08", "ps1", "ps2", "ps4", "dot09"]
     #,"path": ["dot08", "ps1", "ps2", "ps3", "ps4", "dot09"]
     },
    {"id": "f2", "type": "data", "port": 10001, "client": "dot10", "server": "dot11", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": 4
     ,"path": ["dot10", "ps2", "ps4", "dot11"]
     #,"path": ["dot10", "ps1", "ps2", "ps4", "dot11"]
     #,"path": ["dot10", "ps1", "ps2", "ps3", "ps4", "dot11"]
     },
    {"id": "f3", "type": "data", "port": 10002, "client": "dot12", "server": "dot15", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": 4
     ,"path": ["dot12", "ps2", "ps3", "dot15"]
     #,"path": ["dot12", "ps1", "ps2", "ps4", "dot15"]
     #,"path": ["dot12", "ps1", "ps2", "ps3", "ps4", "dot15"]
     },
    {"id": "f4", "type": "data", "port": 10003, "client": "dot20", "server": "dot29", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot20", "ps3", "ps4", "dot29"]
     #,"path": ["dot20", "ps1", "ps2", "ps4", "dot29"]
     #,"path": ["dot20", "ps1", "ps2", "ps3", "ps4", "dot29"]
     },

    # # # COCKPIT CONTROL
    {"id": "f5", "type": "data", "port": 10004, "client": "dot30", "server": "dot31", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     ,"path": ["dot30", "ps2", "ps1", "dot31"]
     #,"path": ["dot30", "ps2", "ps3", "ps4", "dot31"]
     },
    {"id": "f6", "type": "data", "port": 10005, "client": "dot40", "server": "dot120", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     ,"path": ["dot40", "ps4", "ps2", "ps1", "dot120"]
     #,"path": ["dot40", "ps2", "ps3", "ps4", "dot120"]
     },

    # # # ENGINE CONTROL
    {"id": "f7", "type": "data", "port": 10008, "client": "dot140", "server": "dot200", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     ,"path": ["dot140", "ps2", "ps3", "dot200"]
     #,"path": ["dot140", "ps2", "ps3", "ps4", "dot200"]
     },
    {"id": "f8", "type": "data", "port": 10009, "client": "dot220", "server": "dot240", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": 4
     ,"path": ["dot220", "ps3", "ps4", "dot240"]
     #,"path": ["dot220", "ps2", "ps3", "ps4", "dot240"]
     },

    # # # Background
    # {"id": "flaptop", "type": "data", "port": 10013, "client": "dot250", "server": "dot123", "rate": 800,
    #  "data_loc": "/home/iti/", "user": "iti", "priority": 1
    #  ,"path": ["dot250", "ps3", "ps4", "dot123"]
    #  },

    # Time Synchronization Flows
    # This has to be auto-generated in the future

    {"id": "ptp_1_f1", "type": "ptp", "port": 319, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot08", "ps2", "ps4", "dot09"]
     },
    {"id": "ptp_2_f1", "type": "ptp", "port": 320, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot08", "ps2", "ps4", "dot09"]
     },
    {"id": "ptp_3_f1", "type": "ptp", "port": 319, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot09", "ps4", "ps2", "dot08"]
     },
    {"id": "ptp_4_f1", "type": "ptp", "port": 320, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot09", "ps4", "ps2", "dot08"]
     },

    {"id": "ptp_1_f2", "type": "ptp", "port": 319, "client": "dot10", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot10", "ps2", "ps4", "dot11"]
     },
    {"id": "ptp_2_f2", "type": "ptp", "port": 320, "client": "dot10", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot10", "ps2", "ps4", "dot11"]
     },
    {"id": "ptp_3_f2", "type": "ptp", "port": 319, "client": "dot11", "server": "dot10", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot11", "ps4", "ps2", "dot10"]
     },
    {"id": "ptp_4_f2", "type": "ptp", "port": 320, "client": "dot11", "server": "dot10", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot11", "ps4", "ps2", "dot10"]
     },

    {"id": "ptp_1_f3", "type": "ptp", "port": 319, "client": "dot12", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot12", "ps2", "ps3", "dot15"]
     },
    {"id": "ptp_2_f3", "type": "ptp", "port": 320, "client": "dot12", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot12", "ps2", "ps3", "dot15"]
     },
    {"id": "ptp_3_f3", "type": "ptp", "port": 319, "client": "dot15", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot15", "ps3", "ps2", "dot12"]
     },
    {"id": "ptp_4_f3", "type": "ptp", "port": 320, "client": "dot15", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot15", "ps3", "ps2", "dot12"]
     },

    {"id": "ptp_1_f4", "type": "ptp", "port": 319, "client": "dot20", "server": "dot29", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot20", "ps3", "ps4", "dot29"]
     },
    {"id": "ptp_2_f4", "type": "ptp", "port": 320, "client": "dot20", "server": "dot29", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot20", "ps3", "ps4", "dot29"]
     },
    {"id": "ptp_3_f4", "type": "ptp", "port": 319, "client": "dot29", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot29", "ps4", "ps3", "dot20"]
     },
    {"id": "ptp_4_f4", "type": "ptp", "port": 320, "client": "dot29", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot29", "ps4", "ps3", "dot20"]
     },

    {"id": "ptp_1_f5", "type": "ptp", "port": 319, "client": "dot30", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot30", "ps2", "ps1", "dot31"]
     },
    {"id": "ptp_2_f5", "type": "ptp", "port": 320, "client": "dot30", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot30", "ps2", "ps1", "dot31"]
     },
    {"id": "ptp_3_f5", "type": "ptp", "port": 319, "client": "dot31", "server": "dot30", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot31", "ps1", "ps2", "dot30"]
     },
    {"id": "ptp_4_f5", "type": "ptp", "port": 320, "client": "dot31", "server": "dot30", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot31", "ps1", "ps2", "dot30"]
     },

    {"id": "ptp_1_f6", "type": "ptp", "port": 319, "client": "dot40", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot40", "ps4", "ps2", "ps1", "dot120"]
     },
    {"id": "ptp_2_f6", "type": "ptp", "port": 320, "client": "dot40", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot40", "ps4", "ps2", "ps1", "dot120"]
     },
    {"id": "ptp_3_f6", "type": "ptp", "port": 319, "client": "dot120", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot120", "ps1", "ps2", "ps4", "dot40"]
     },
    {"id": "ptp_4_f6", "type": "ptp", "port": 320, "client": "dot120", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot120", "ps1", "ps2", "ps4", "dot40"]
     },

    {"id": "ptp_1_f7", "type": "ptp", "port": 319, "client": "dot140", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot140", "ps2", "ps3", "dot200"]
     },
    {"id": "ptp_2_f7", "type": "ptp", "port": 320, "client": "dot140", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot140", "ps2", "ps3", "dot200"]
     },
    {"id": "ptp_3_f7", "type": "ptp", "port": 319, "client": "dot200", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot200", "ps3", "ps2", "dot140"]
     },
    {"id": "ptp_4_f7", "type": "ptp", "port": 320, "client": "dot200", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot200", "ps3", "ps2", "dot140"]
     },

    {"id": "ptp_1_f8", "type": "ptp", "port": 319, "client": "dot220", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot220", "ps3", "ps4", "dot240"]
     },
    {"id": "ptp_2_f8", "type": "ptp", "port": 320, "client": "dot220", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot220", "ps3", "ps4", "dot240"]
     },
    {"id": "ptp_3_f8", "type": "ptp", "port": 319, "client": "dot240", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot240", "ps4", "ps3", "dot220"]
     },
    {"id": "ptp_4_f8", "type": "ptp", "port": 320, "client": "dot240", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot240", "ps4", "ps3", "dot220"]
     },

    {"id": "ptp_1_flaptop", "type": "ptp", "port": 319, "client": "dot250", "server": "dot123", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot250", "ps3", "ps4", "dot123"]
     },
    {"id": "ptp_2_flaptop", "type": "ptp", "port": 320, "client": "dot250", "server": "dot123", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot250", "ps3", "ps4", "dot123"]
     },
    {"id": "ptp_3_flaptop", "type": "ptp", "port": 319, "client": "dot123", "server": "dot250", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot123", "ps4", "ps3", "dot250"]
     },
    {"id": "ptp_4_flaptop", "type": "ptp", "port": 320, "client": "dot123", "server": "dot250", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": 7,
     "path": ["dot123", "ps4", "ps3", "dot250"]
     },

]