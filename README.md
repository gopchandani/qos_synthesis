### How do I get set up? ###

* If you don't have pip installed, then install the python package manager. (Ubuntu package: python-pip)
* Ensure that the RYU version you install is 4.0
* Ensure that you have OVS version 2.3.0 installed.
* sudo pip install ryu
* sudo pip install networkx
* sudo pip install netaddr
* sudo pip install intervaltree
* sudo pip install httplib2
* Install mininet version 2.2 by following instructions here: http://mininet.org/download/
* sudo apt-get install python-scipy
* sudo apt-get install python-numpy
* sudo apt-get install python-matplotlib
* Setup PYTHONPATH to src folder by adding following to ~/.bashrc: export PYTHONPATH=${PYTHONPATH}:/home/flow/flow_validator/src/ and allow PYTHONPATH to be retained by sudo by adding following to /etc/sudoers: Defaults env_keep += "PYTHONPATH"
* For running, go under src/experiments and run: sudo python experiment_module_name.py
* Install netperf from its source (http://www.netperf.org/netperf/DownloadNetperf.html) with following compile options enabled(./configure --enable-intervals --enable-burst --enable-demo --enable-omni)

### If your Ryu doesn't work because of missing dependencies, you might also need to run following ###
* sudo pip install rfc3986
* sudo pip install stevedore
* sudo pip install debtcollector
* sudo pip install oslo.i18n
* sudo pip install greenlet


### Who do I talk to? ###

* Rakesh Kumar (kumar19@illinois.edu)