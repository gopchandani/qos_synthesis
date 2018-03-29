
# Place all traces for the Multiplexing expeirments

Trace 1: Switch Processing Time

The excel file SwitchProcessingTime contains two excel sheets. The sheet 'Final Data' contains the data for
processing time as a function of packet sizes. This sheet also contains the end-to-end delay (also
called the one-way trip time) from source to destination.

One Way Time(1 switch) refers to the topology host-switch-host
One Way Time(2 switches) refers to the topology host-switch-switch-host

We do this to for packet sizes: 400 bytes, 512 bytes and 1024 bytes.

Observations
------------

1) The packet size definitely has an impact on the processing time in the switch.
It increases with increasing packet size.
2) Since processing time in the switch affects the one-way trip time, packet size
impacts one-way trip time as well.

