#!/bin/sh

tc=/sbin/tc
ext=em1
#ext_ingress=ifb0

$tc qdisc add dev $ext root handle 1: htb default 11 r2q 1
$tc class add dev $ext parent 1: classid 1:1 htb rate 120bps ceil 120bps 
$tc class add dev $ext parent 1:1 classid 1:10 htb rate 45bps ceil 120bps prio 0

# Add filter - ICMP packet
tc filter add dev $ext protocol ip parent 1:0 prio 0 u32 \
   match ip protocol 1 0xff flowid 1:10

