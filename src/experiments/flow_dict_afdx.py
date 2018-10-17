
all_flows = [
    # FLIGHT CONTROL
    
    {"id": "f1", "type": "data", "port": 10000, "client": "dot15", "server": "dot240", "rate": 4,
     "data_loc": "/home/pi/", "user": "pi", "priority":5
     #,"path": ["dot08", "ps1", "ps4", "dot09"]
     #,"path": ["dot08", "ps1", "ps2", "ps4", "dot09"]
     #,"path": ["dot08", "ps1", "ps2", "ps3", "ps4", "dot09"]
     },
    {"id": "f2", "type": "data", "port": 10001, "client": "dot20", "server": "dot242", "rate": 4,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     #,"path": ["dot10", "ps1", "ps4", "dot11"]
     #,"path": ["dot10", "ps1", "ps2", "ps4", "dot11"]
     #,"path": ["dot10", "ps1", "ps2", "ps3", "ps4", "dot11"]
     },
    {"id": "f3", "type": "data", "port": 10002, "client": "dot29", "server": "dot120", "rate": 4,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     #,"path": ["dot12", "ps1", "ps4", "dot15"]
     #,"path": ["dot12", "ps1", "ps2", "ps4", "dot15"]
     #,"path": ["dot12", "ps1", "ps2", "ps3", "ps4", "dot15"]
     },
    {"id": "f4", "type": "data", "port": 10003, "client": "dot140", "server": "dot244", "rate": 4,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     #,"path": ["dot20", "ps1", "ps4", "dot29"]
     #,"path": ["dot20", "ps1", "ps2", "ps4", "dot29"]
     #,"path": ["dot20", "ps1", "ps2", "ps3", "ps4", "dot29"]
     },
    
    # COCKPIT CONTROL
    {"id": "f5", "type": "data", "port": 10004, "client": "dot12", "server": "dot08", "rate": 4,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     #,"path": ["dot30", "ps2", "ps4", "dot31"]
     #,"path": ["dot30", "ps2", "ps3", "ps4", "dot31"]
     },
    {"id": "f6", "type": "data", "port": 10005, "client": "dot220", "server": "dot09", "rate": 4,
     "data_loc": "/home/pi/", "user": "pi", "priority": 5
     #,"path": ["dot40", "ps2", "ps4", "dot120"]
     #,"path": ["dot40", "ps2", "ps3", "ps4", "dot120"]
     },
    
    # ENGINE CONTROL
    {"id": "f7", "type": "data", "port": 10006, "client": "dot11", "server": "dot31", "rate": 4,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     #,"path": ["dot140", "ps2", "ps4", "dot200"]
     #,"path": ["dot140", "ps2", "ps3", "ps4", "dot200"]
     },
    {"id": "f8", "type": "data", "port": 10007, "client": "dot40", "server": "dot200", "rate": 4,
     "data_loc": "/home/pi/", "user": "pi", "priority": 6
     #,"path": ["dot220", "ps2", "ps4", "dot240"]
     #,"path": ["dot220", "ps2", "ps3", "ps4", "dot240"]
     },


    # Time Synchronization Flows
    # This has to be auto-generated in the future

    {"id": "ptp_1_f1", "type": "ptp", "port": 319, "client": "dot15", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f1", "type": "ptp", "port": 320, "client": "dot15", "server": "dot240", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f1", "type": "ptp", "port": 319, "client": "dot240", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f1", "type": "ptp", "port": 320, "client": "dot240", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f2", "type": "ptp", "port": 319, "client": "dot20", "server": "dot242", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f2", "type": "ptp", "port": 320, "client": "dot20", "server": "dot242", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f2", "type": "ptp", "port": 319, "client": "dot242", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f2", "type": "ptp", "port": 320, "client": "dot242", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f3", "type": "ptp", "port": 319, "client": "dot29", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f3", "type": "ptp", "port": 320, "client": "dot29", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f3", "type": "ptp", "port": 319, "client": "dot120", "server": "dot29", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f3", "type": "ptp", "port": 320, "client": "dot120", "server": "dot29", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f4", "type": "ptp", "port": 319, "client": "dot140", "server": "dot244", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f4", "type": "ptp", "port": 320, "client": "dot140", "server": "dot244", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f4", "type": "ptp", "port": 319, "client": "dot244", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f4", "type": "ptp", "port": 320, "client": "dot244", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f5", "type": "ptp", "port": 319, "client": "dot12", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f5", "type": "ptp", "port": 320, "client": "dot12", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f5", "type": "ptp", "port": 319, "client": "dot08", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f5", "type": "ptp", "port": 320, "client": "dot08", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f6", "type": "ptp", "port": 319, "client": "dot220", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f6", "type": "ptp", "port": 320, "client": "dot220", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f6", "type": "ptp", "port": 319, "client": "dot09", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f6", "type": "ptp", "port": 320, "client": "dot09", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f7", "type": "ptp", "port": 319, "client": "dot11", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f7", "type": "ptp", "port": 320, "client": "dot11", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f7", "type": "ptp", "port": 319, "client": "dot31", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f7", "type": "ptp", "port": 320, "client": "dot31", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

    {"id": "ptp_1_f8", "type": "ptp", "port": 319, "client": "dot40", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_2_f8", "type": "ptp", "port": 320, "client": "dot40", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_3_f8", "type": "ptp", "port": 319, "client": "dot200", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },
    {"id": "ptp_4_f8", "type": "ptp", "port": 320, "client": "dot200", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     },

 ]




