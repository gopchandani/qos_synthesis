#include <time.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <limits.h>

#define BILLION 1000000000L

/*
 * error - wrapper for perror
 */
void error(char *msg) {
	perror(msg);
	exit(1);
}

struct packet_message{
	int id;
	struct timespec snapshot;
	char payload[984];
};

long int *secs;
long int *nanosecs;
int count = 0;
int sockfd; /* socket */

void print_data() {

	int i = 0;
	for (i=0; i < count; i ++ )
	{
		printf("\n%ld, %d, %ld, %ld, %ld, %ld", 0, 0, secs[i], nanosecs[i], 0, 0);
	}
	printf("\n");
}

void handle_sigint(int sig) {
	shutdown(sockfd, SHUT_RDWR);
	print_data();
	exit(0);
}

int main(int argc, char **argv) {

	if (argc == 2 && strcmp(argv[1], "--help")==0 ){
        	printf("Time Measurement Tool: Server Side\n");
        	printf("Usage : ./server <server-port-number> <number-packets>\n");
        	return 0;
	}
	
	signal(SIGINT, handle_sigint);

	int portno; /* port to listen on */

	int number_time_packets = atoi(argv[2]);
	
	secs = malloc(number_time_packets * sizeof(long int));
	nanosecs = malloc(number_time_packets * sizeof(long int));

	memset(secs, 0, number_time_packets * sizeof(long int));
	memset(nanosecs, 0, number_time_packets * sizeof(long int));

	int clientlen; /* byte size of client's address */
	struct sockaddr_in serveraddr; /* server's addr */
	struct sockaddr_in clientaddr; /* client addr */
	
	struct timespec receive_timestamp;
	struct timespec local_timestamp;
	struct packet_message *temp = malloc(sizeof(struct packet_message));
	//FILE *fp = fopen(argv[2], "a");

	int one_way_seconds;
	long int one_way_nanoseconds;

	long int running_average_one_way[2] = {0, 0};
	long int worst_case_one_way[2] = {0,0};
	long int num_packets_seen[2] = {0, 0};

	int pkt_id;

	struct hostent *hostp; /* client host info */
	char *hostaddrp; /* dotted decimal host addr string */
	int optval; /* flag value for setsockopt */
	int n; /* message byte size */


	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd < 0) 
		error("ERROR opening socket");

	/* setsockopt: Handy debugging trick that lets 
	* us rerun the server immediately after we kill it; 
	* otherwise we have to wait about 20 secs. 
	* Eliminates "ERROR on binding: Address already in use" error. 
	*/

	optval = 1;
	setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, \
		(const void *)&optval , sizeof(int));

	/*
   	* build the server's Internet address
	*/

	bzero((char *) &serveraddr, sizeof(serveraddr));
	portno = atoi(argv[1]);
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serveraddr.sin_port = htons((unsigned short)portno);

	/* 
	* bind: associate the parent socket with a port 
	*/
  	if (bind(sockfd, (struct sockaddr *) &serveraddr, sizeof(serveraddr)) < 0) 
		error("ERROR on binding");


	clientlen = sizeof(clientaddr);
	printf("\nHost ID, Packet Number, One-way delay(s), One-way delay(ns), Running Avg.(ns), Worst-case(ns)"); 

	while (count < number_time_packets){
	/*
	* recvfrom: receive a UDP datagram from a client
	*/
		recvfrom(sockfd, (void *)temp, sizeof(struct packet_message), 0,(struct sockaddr *) &clientaddr, &clientlen);
		pkt_id = temp->id;
	
		clock_gettime(CLOCK_REALTIME, &local_timestamp);
		receive_timestamp.tv_sec = temp->snapshot.tv_sec;
		receive_timestamp.tv_nsec = temp->snapshot.tv_nsec;
				
		one_way_seconds = (local_timestamp.tv_sec - receive_timestamp.tv_sec);
		one_way_nanoseconds = (local_timestamp.tv_nsec - receive_timestamp.tv_nsec);
	
	        if(one_way_seconds < 0)
			one_way_seconds += INT_MAX;

        	if(one_way_nanoseconds < 0)
			one_way_nanoseconds += LONG_MAX ;

		secs[count] = one_way_seconds;
		nanosecs[count] = one_way_nanoseconds;
		count = count + 1;

	}

	shutdown(sockfd, SHUT_RDWR);
	print_data();
	return 0;

}
