import time
import os
from flow_dict import all_flows as flows

#from synthesis.synthesis_lib_hardware import SynthesisLibHardware

#
# synthesis_lib = SynthesisLibHardware(None)
#
# def synthesize_flow(f):
#     pass


flow_cmds = []

def populate_flow_cmds():

    cmd = "ovs-ofctl add-flow " + \
                   "tcp:" + "" + ":" + bridge_dict["of_port"] + " " \
                   "in_port=" + str(in_port.split('/')[2]) +  \
                   ",dl_dst=" + dst_mac + \
                    ",vlan_vid=0x1000/0x1000" + "," + \
                    "actions=strip_vlan," + "output:" + str(out_port.split('/')[2])
                    #"set_queue:" + str(q_id) + ","\

    flow_cmds.append(cmd)

def trigger():
    populate_flow_cmds()
    for cmd in flow_cmds:
        os.system(cmd)
        time.sleep(1)


if __name__ == "__main__":
    trigger()
