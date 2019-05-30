## Higher number means higher priority

ptp_priority = 7
high_priority = 6
medium_priority = 5
low_priority = 4
background_priority = 0


all_flows = [
    # FLIGHT CONTROL
    {"id": "f1", "type": "data", "port": 10000, "client": "dot08", "server": "dot09", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority":low_priority
     ,"path": ["dot08", "ps2", "ps4", "dot09"]
     #,"path": ["dot08", "ps1", "ps2", "ps4", "dot09"]
     #,"path": ["dot08", "ps1", "ps2", "ps3", "ps4", "dot09"]
     },
    {"id": "f2", "type": "data", "port": 10001, "client": "dot10", "server": "dot11", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": low_priority
     ,"path": ["dot10", "ps2", "ps4", "dot11"]
     #,"path": ["dot10", "ps1", "ps2", "ps4", "dot11"]
     #,"path": ["dot10", "ps1", "ps2", "ps3", "ps4", "dot11"]
     },
    {"id": "f3", "type": "data", "port": 10002, "client": "dot12", "server": "dot15", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": low_priority
     ,"path": ["dot12", "ps2", "ps3", "dot15"]
     #,"path": ["dot12", "ps1", "ps2", "ps4", "dot15"]
     #,"path": ["dot12", "ps1", "ps2", "ps3", "ps4", "dot15"]
     },
    {"id": "f4", "type": "data", "port": 10003, "client": "dot20", "server": "dot244", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": low_priority
     ,"path": ["dot20", "ps3", "ps4", "dot244"]
     #,"path": ["dot20", "ps1", "ps2", "ps4", "dot29"]
     #,"path": ["dot20", "ps1", "ps2", "ps3", "ps4", "dot29"]
     },

    # # # COCKPIT CONTROL
    {"id": "f5", "type": "data", "port": 10004, "client": "dot30", "server": "dot31", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": medium_priority
     ,"path": ["dot30", "ps2", "ps1", "dot31"]
     #,"path": ["dot30", "ps2", "ps3", "ps4", "dot31"]
     },
    {"id": "f6", "type": "data", "port": 10005, "client": "dot40", "server": "dot120", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": medium_priority
     ,"path": ["dot40", "ps4", "ps2", "ps1", "dot120"]
     #,"path": ["dot40", "ps2", "ps3", "ps4", "dot120"]
     },

    # # # ENGINE CONTROL
    {"id": "f7", "type": "data", "port": 10008, "client": "dot140", "server": "dot200", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": high_priority
     ,"path": ["dot140", "ps2", "ps3", "dot200"]
     #,"path": ["dot140", "ps2", "ps3", "ps4", "dot200"]
     },
    {"id": "f8", "type": "data", "port": 10009, "client": "dot220", "server": "dot248", "rate": 88,
     "data_loc": "/home/pi/", "user": "pi", "priority": high_priority
     ,"path": ["dot220", "ps3", "ps4", "dot248"]
     #,"path": ["dot220", "ps2", "ps3", "ps4", "dot240"]
     },

    # # # Background
    # {"id": "flaptop", "type": "data", "port": 10013, "client": "dot250", "server": "dot123", "rate": 800,
    #  "data_loc": "/home/iti/", "user": "iti", "priority": background_priority
    #  ,"path": ["dot250", "ps3", "ps4", "dot123"]
    #  },

    # Time Synchronization Flows
    # This has to be auto-generated in the future

    {"id": "ptp_1_f1", "type": "ptp", "port": 319, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot08", "ps2", "ps4", "dot09"]
     },
    {"id": "ptp_2_f1", "type": "ptp", "port": 320, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot08", "ps2", "ps4", "dot09"]
     },
    {"id": "ptp_3_f1", "type": "ptp", "port": 319, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot09", "ps4", "ps2", "dot08"]
     },
    {"id": "ptp_4_f1", "type": "ptp", "port": 320, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot09", "ps4", "ps2", "dot08"]
     },

    {"id": "ptp_1_f2", "type": "ptp", "port": 319, "client": "dot10", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot10", "ps2", "ps4", "dot11"]
     },
    {"id": "ptp_2_f2", "type": "ptp", "port": 320, "client": "dot10", "server": "dot11", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot10", "ps2", "ps4", "dot11"]
     },
    {"id": "ptp_3_f2", "type": "ptp", "port": 319, "client": "dot11", "server": "dot10", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot11", "ps4", "ps2", "dot10"]
     },
    {"id": "ptp_4_f2", "type": "ptp", "port": 320, "client": "dot11", "server": "dot10", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot11", "ps4", "ps2", "dot10"]
     },

    {"id": "ptp_1_f3", "type": "ptp", "port": 319, "client": "dot12", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot12", "ps2", "ps3", "dot15"]
     },
    {"id": "ptp_2_f3", "type": "ptp", "port": 320, "client": "dot12", "server": "dot15", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot12", "ps2", "ps3", "dot15"]
     },
    {"id": "ptp_3_f3", "type": "ptp", "port": 319, "client": "dot15", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot15", "ps3", "ps2", "dot12"]
     },
    {"id": "ptp_4_f3", "type": "ptp", "port": 320, "client": "dot15", "server": "dot12", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot15", "ps3", "ps2", "dot12"]
     },

    {"id": "ptp_1_f4", "type": "ptp", "port": 319, "client": "dot20", "server": "dot244", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot20", "ps3", "ps4", "dot244"]
     },
    {"id": "ptp_2_f4", "type": "ptp", "port": 320, "client": "dot20", "server": "dot244", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot20", "ps3", "ps4", "dot244"]
     },
    {"id": "ptp_3_f4", "type": "ptp", "port": 319, "client": "dot244", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot244", "ps4", "ps3", "dot20"]
     },
    {"id": "ptp_4_f4", "type": "ptp", "port": 320, "client": "dot244", "server": "dot20", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot244", "ps4", "ps3", "dot20"]
     },

    {"id": "ptp_1_f5", "type": "ptp", "port": 319, "client": "dot30", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot30", "ps2", "ps1", "dot31"]
     },
    {"id": "ptp_2_f5", "type": "ptp", "port": 320, "client": "dot30", "server": "dot31", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot30", "ps2", "ps1", "dot31"]
     },
    {"id": "ptp_3_f5", "type": "ptp", "port": 319, "client": "dot31", "server": "dot30", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot31", "ps1", "ps2", "dot30"]
     },
    {"id": "ptp_4_f5", "type": "ptp", "port": 320, "client": "dot31", "server": "dot30", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot31", "ps1", "ps2", "dot30"]
     },

    {"id": "ptp_1_f6", "type": "ptp", "port": 319, "client": "dot40", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot40", "ps4", "ps2", "ps1", "dot120"]
     },
    {"id": "ptp_2_f6", "type": "ptp", "port": 320, "client": "dot40", "server": "dot120", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot40", "ps4", "ps2", "ps1", "dot120"]
     },
    {"id": "ptp_3_f6", "type": "ptp", "port": 319, "client": "dot120", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot120", "ps1", "ps2", "ps4", "dot40"]
     },
    {"id": "ptp_4_f6", "type": "ptp", "port": 320, "client": "dot120", "server": "dot40", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot120", "ps1", "ps2", "ps4", "dot40"]
     },

    {"id": "ptp_1_f7", "type": "ptp", "port": 319, "client": "dot140", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot140", "ps2", "ps3", "dot200"]
     },
    {"id": "ptp_2_f7", "type": "ptp", "port": 320, "client": "dot140", "server": "dot200", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot140", "ps2", "ps3", "dot200"]
     },
    {"id": "ptp_3_f7", "type": "ptp", "port": 319, "client": "dot200", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot200", "ps3", "ps2", "dot140"]
     },
    {"id": "ptp_4_f7", "type": "ptp", "port": 320, "client": "dot200", "server": "dot140", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot200", "ps3", "ps2", "dot140"]
     },

    {"id": "ptp_1_f8", "type": "ptp", "port": 319, "client": "dot220", "server": "dot248", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot220", "ps3", "ps4", "dot248"]
     },
    {"id": "ptp_2_f8", "type": "ptp", "port": 320, "client": "dot220", "server": "dot248", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot220", "ps3", "ps4", "dot248"]
     },
    {"id": "ptp_3_f8", "type": "ptp", "port": 319, "client": "dot248", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot248", "ps4", "ps3", "dot220"]
     },
    {"id": "ptp_4_f8", "type": "ptp", "port": 320, "client": "dot248", "server": "dot220", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":ptp_priority,
     "path": ["dot248", "ps4", "ps3", "dot220"]
     },

    {"id": "ptp_1_flaptop", "type": "ptp", "port": 319, "client": "dot250", "server": "dot123", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": ptp_priority,
     "path": ["dot250", "ps3", "ps4", "dot123"]
     },
    {"id": "ptp_2_flaptop", "type": "ptp", "port": 320, "client": "dot250", "server": "dot123", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": ptp_priority,
     "path": ["dot250", "ps3", "ps4", "dot123"]
     },
    {"id": "ptp_3_flaptop", "type": "ptp", "port": 319, "client": "dot123", "server": "dot250", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": ptp_priority,
     "path": ["dot123", "ps4", "ps3", "dot250"]
     },
    {"id": "ptp_4_flaptop", "type": "ptp", "port": 320, "client": "dot123", "server": "dot250", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority": ptp_priority,
     "path": ["dot123", "ps4", "ps3", "dot250"]
     },

]