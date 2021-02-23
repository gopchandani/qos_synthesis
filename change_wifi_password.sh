#!/bin/sh

oldpass_hash=`echo -n "$1" | iconv -t UTF-16LE | openssl md4 | cut -d' ' -f2`
echo $oldpass_hash
newpass_hash=`echo -n "$2" | iconv -t UTF-16LE | openssl md4 | cut -d' ' -f2`
echo $newpass_hash
file="/etc/wpa_supplicant/wpa_supplicant.conf.bak"
sudo sed -i "s/${oldpass_hash}/${newpass_hash}/" ${file}
