#--
#load the module
ext=em1
modprobe ifb
modprobe act_mirred
ethtool -K $ext tso off gso off gro off


