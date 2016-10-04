#README

* A nice tutorial and installation instruction for IFB
`https://wiki.gentoo.org/wiki/Traffic_shaping`

In the Glacier, I had checked earlier, IFB module option is already selected, so no need to go through the installtion. You can start using the script. 

* See queue discipline of an interface
	* tc qdisc show dev eth1
* See the class details for an interface
	* tc -s -d class show dev eth1
	* tc -s -d class show dev ifb0
* Experiment Scripts

	* htb_exp.sh - It installs HTB qdisc for egress with 3 classes - class1 (ICMP protocol), class 2 (ssh traffic), class 3 is the default
	* ifb_htb.sh - It adds pesudo interface ifb0 to the ingress of eth1, installs HTB qdisc for the egress of ifb0 with three classes,
	installs HTB qdisc for egress of eth1 with three classes.
	* delete_interface.sh - deletes all qdiscs settings. Use this everytime when you want to change the htb rates or priority and run the htb_exp.sh script or ifb_htb.sh script.   

* All scripts required to be executed with sudo

* To test the scripts - 

	* Change the src ip address in the script based on your machine ip address
	* Run the script
	* Test if the qdisc and classes information by using the commands mentioned above.	At this point,
	you should be able to see the htb qdisc has been attached to the interface with all class rates information,
	number of packets sent, yokens info, etc.
	* To test if classification works- ping -c 5 IP address of your machine. You should able to see 5 packets in the class 1:10 based on the script
	* To test for SSH traffic - sftp from another machine to your machine in which you attached htb qdisc to the interface. put some file. you should be able to number of packets in the class 1:12 using the above tc class command.
	* Note that in the ifb_htb.sh, TCP traffic are sent to class 1:12 irrespective of any port number.
	* Also, the rates in the scripts are deliberately kept low to see the classification and rate limit affect.
	If you have sshed to your machine through several terminals,
	the terminal windows might get very slow owing to the low rate of ssh traffic set by the script,
	sometimes ssh connection drops. So in that case just execute the delete_interface.sh.
	Then you can edit the script to high rate and can start the experiment fresh.
   


