
all_flows = [
    {"id": "f1", "type": "data", "port": 10000, "client": "dot08", "server": "dot09", "rate":80,
     "data_loc": "/home/pi/", "user": "pi", "priority":6
     ,"path": ["dot08", "ps1", "dot09"]
     },

    # {"id": "flaptop", "type": "data", "port": 10013, "client": "dot250", "server": "dot123", "rate": 5,
    #  "data_loc": "/home/iti/", "user": "iti", "priority": 1
    #  ,"path": ["dot250", "ps1", "ps2", "ps3", "ps4", "dot123"]
    #  },

    # Time Synchronization Flows
    # This has to be auto-generated in the future

    {"id": "ptp_1_f1", "type": "ptp", "port": 319, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot08", "ps1", "dot09"]
     },
    {"id": "ptp_2_f1", "type": "ptp", "port": 320, "client": "dot08", "server": "dot09", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot08", "ps1", "dot09"]
     },
    {"id": "ptp_3_f1", "type": "ptp", "port": 319, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot09", "ps1", "dot08"]
     },
    {"id": "ptp_4_f1", "type": "ptp", "port": 320, "client": "dot09", "server": "dot08", "rate": 50,
     "data_loc": "/home/pi/", "user": "pi", "priority":7,
     "path": ["dot09", "ps1", "dot08"]
     },

]