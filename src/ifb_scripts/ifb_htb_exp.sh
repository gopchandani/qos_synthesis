#!/bin/sh

tc=/sbin/tc
ext=em1
ext_ingress=ifb0

#-- Class rate limits set up
htb_rate=140bps
class1_rate=65bps
class1_max_rate=140bps

class2_rate=65bps
class2_max_rate=140bps

class3_rate=10bps
class3_max_rate=140bps
#--
#load the module
modprobe ifb
modprobe act_mirred
ethtool -K $ext tso off gso off gro off


#---INGRESS--
$tc qdisc add dev $ext handle ffff: ingress
ifconfig $ext_ingress up
$tc filter add dev $ext parent ffff: protocol all u32 match u32 0 0 action mirred egress redirect dev $ext_ingress

# create htb qdisc and add three classes with handle :10, :11, :12. Default is :11 
# 'prio' value decide on the priority of the traffic
$tc qdisc add dev $ext_ingress root handle 1: htb default 11 r2q 1
$tc class add dev $ext_ingress parent 1: classid 1:1 htb rate $htb_rate ceil $htb_rate 
$tc class add dev $ext_ingress parent 1:1 classid 1:10 htb rate $class1_rate ceil $class1_max_rate prio 0
$tc class add dev $ext_ingress parent 1:1 classid 1:11 htb rate $class3_rate ceil $class3_max_rate prio 2
$tc class add dev $ext_ingress parent 1:1 classid 1:12 htb rate $class2_rate ceil $class2_max_rate prio 1

# Add filter - ICMP packet
tc filter add dev $ext_ingress protocol ip parent 1:0 prio 1 u32 \
   match ip protocol 1 0xff flowid 1:10

# Add filter - SSH Traffic
tc filter add dev $ext_ingress protocol ip parent 1:0 prio 0 u32 \
match ip protocol 6 0xff flowid 1:12

#---EGRESS--
$tc qdisc add dev $ext root handle 1: htb default 11 r2q 1
$tc class add dev $ext parent 1: classid 1:1 htb rate $htb_rate ceil $htb_rate   
$tc class add dev $ext parent 1:1 classid 1:10 htb rate $class1_rate ceil $class1_max_rate prio 0
$tc class add dev $ext parent 1:1 classid 1:11 htb rate $class3_rate ceil $class3_max_rate prio 2
$tc class add dev $ext parent 1:1 classid 1:12 htb rate $class2_rate ceil $class2_max_rate prio 1

# Add filter - ICMP packet
tc filter add dev $ext protocol ip parent 1:0 prio 1 u32 \
   match ip protocol 1 0xff flowid 1:10

# Add filter - SSH Traffic
tc filter add dev $ext protocol ip parent 1:0 prio 0 u32 match ip src 130.126.138.46 \
match ip sport 22 0xffff flowid 1:12

