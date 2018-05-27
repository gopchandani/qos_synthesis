
from data_summary import get_data_dict, periods_str, num_switches_strs, payloads_strs
data_dict = get_data_dict()


# Processing time estimate using end-to-end delays
# Get for the payload sizes: 256B and 1408B and packet periods 100ms and 1000ms
# Take the mean end-to-end delay for four switches (fs) and single switch(ss)
# Then, amortized switch processing time = (fs - ss) / 3

# fs = data_dict['100ms']['4']['256B']["mean"]
# ss = data_dict['100ms']['1']['256B']["mean"]
#
# print("Time with Laptops @ 100ms, 256B:", (fs - ss)/3)
#
# fs = data_dict['1000ms']['4']['256B']["mean"]
# ss = data_dict['1000ms']['1']['256B']["mean"]
#
# print("Time with Pis @ 1000ms, 256B:", (fs - ss)/3)


# fs = data_dict['100ms']['4']['1024B']["mean"]
# ss = data_dict['100ms']['1']['1024B']["mean"]
#
# print("Time with Laptops @ 100ms, 1024B:", (fs - ss)/3)

fs = data_dict['1000ms']['4']['1024B']["mean"]
ss = data_dict['1000ms']['1']['1024B']["mean"]

print("Time with Pis @ 1000ms, 1024B:", (fs - ss)/3)

#
#
# fs = data_dict['100ms']['4']['1408B']["mean"]
# ss = data_dict['100ms']['1']['1408B']["mean"]
# print("Time with Laptops @ 100ms, 1408B:", (fs - ss)/3)
#
# fs = data_dict['1000ms']['4']['1408B']["mean"]
# ss = data_dict['1000ms']['1']['1408B']["mean"]
# print("Time with Pis @ 1000ms, 1408B:", (fs - ss)/3)
#
