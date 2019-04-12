#include<unistd.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<stdio.h>
#include<arpa/inet.h>
#include<string.h>
#include<time.h>
#include<stdlib.h>

struct packet_message{
    int id;
    struct timespec snapshot;
    char payload[984];
};

unsigned long int count = 0;
/*double *send_times;

void print_data() {

        int i = 0;
        for (i=0; i < count; i ++ )
        {
                printf("\nSend time = %lf", send_times[i]);
        }
        printf("\n");
}
*/

int main(int argc, char *argv[]){

    if (argc == 2 && strcmp(argv[1], "--help")==0 ){
	printf("Time Measurement Tool: Client Side\n");
	printf("Usage : ./client <server-ip> <number-packets> <budget-us> <udp port> \n");
	return 0;
    }    

    int udp_socket;
    unsigned long int number_time_packets = atoi(argv[2]);
    long int send_time;
    struct timespec end_timestamp;
    struct timespec send_timestamp;

    struct packet_message *pack_msg = malloc(sizeof(struct packet_message));

    if ( (udp_socket = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        perror("socket failed");
        return 1;
    }

    struct sockaddr_in serveraddr;
    memset (&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(atoi(argv[4]));              

    if(inet_pton(AF_INET, argv[1], &serveraddr.sin_addr)<=0)
    {
        printf("\n inet_pton error occured\n");
        return 1;
    } 
    
    long int budget_for_rate = atoi(argv[3]);

    while(count < number_time_packets){
	
	if (count % 1000 == 0) {
        	printf("\ncount: %d/%d", count, number_time_packets);
 	}	

	clock_gettime(CLOCK_REALTIME, &send_timestamp);
	pack_msg->id = count++;
	pack_msg->snapshot = send_timestamp;

	if(sendto(udp_socket, (void *)pack_msg, sizeof(struct packet_message), 0, (struct sockaddr *)&serveraddr, sizeof(serveraddr)) < 0){
		perror("sendto failure!\n");
		break;
	}
	clock_gettime(CLOCK_REALTIME, &end_timestamp);
	send_time = end_timestamp.tv_nsec - send_timestamp.tv_nsec;
  	
	if (budget_for_rate - send_time > 0)
	{
		usleep((budget_for_rate - send_time) / 1000);
	}
    }
    
    close(udp_socket);
    return 0;
} 
