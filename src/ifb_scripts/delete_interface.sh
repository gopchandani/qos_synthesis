#!/bin/sh

tc=/sbin/tc
ext=eth1                # Change for your device!
ext_ingress=ifb0   
$tc qdisc del dev $ext root
$tc qdisc del dev $ext ingress
$tc qdisc del dev $ext_ingress root
#$tc qdisc del dev $ext_ingress ingress
