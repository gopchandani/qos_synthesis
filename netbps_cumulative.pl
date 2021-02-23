#!/usr/bin/perl
use strict;
use warnings;
use Time::HiRes;

my $reporting_interval = 10; # seconds
my $bytes_this_interval = 0;
my $bytes_total = 0;
my $start_time = [Time::HiRes::gettimeofday()];
my $avg_Mbps = 0;
my $count=0;
STDOUT->autoflush(1);

while (<>) {
  if (/ length (\d+):/) {

    $bytes_this_interval += $1;

    my $elapsed_seconds = Time::HiRes::tv_interval($start_time);
    if ($elapsed_seconds > $reporting_interval) {
       my $bps = $bytes_this_interval / $elapsed_seconds;
       my $Mbps = ($bps*8)/(1000*1024);
       if ($count != 0){
           $avg_Mbps = (($count - 1)*$avg_Mbps + $Mbps)/$count;
       }
       printf "count = %d %02d:%02d:%02d %10.2f Mbps Avg=%10.2f \n", $count, (localtime())[2,1,0],$Mbps,$avg_Mbps;
       $count += 1;
       #printf "%02d:%02d:%02d %10.2f Mbps\n", (localtime())[2,1,0],$bps;
       $start_time = [Time::HiRes::gettimeofday()];
       $bytes_total = $bytes_total + $bytes_this_interval;
       printf "Cumulative Average = %10.2f Mbps\n", ($bytes_total*8)/(1E6 * $count * $reporting_interval);
       $bytes_this_interval = 0;
    }
  }
}
