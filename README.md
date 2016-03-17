### How do I get set up? ###

* If you don't have pip installed, then install the python package manager. (Ubuntu package: python-pip)
* Ensure that the RYU version you install is 3.20 (it is an older version)
* Ensure that you have OVS version 2.1.0 installed.
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

### Who do I talk to? ###

* Rakesh Kumar (kumar19@illinois.edu)
