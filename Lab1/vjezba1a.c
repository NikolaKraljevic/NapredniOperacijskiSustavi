 #include <stdio.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

struct msgbuf_t{
	long  mtype;
	char 	 mtex[128];
};

void posjetitelj(int pid,int msg_id,int msg_id2){
	srand(getpid());
	long prvi = pid;
	long drugi = pid;
	prvi +=8;
	drugi +=16;
	struct msgbuf_t msg_rcv,msg_snd;
	for(int i = 0;i<3;i++){
		int brojneki = rand()%1900000+100000;
		usleep(brojneki);
		msg_snd.mtype = pid;
		
		strcpy(msg_snd.mtex,"Zelim se voziti");
		
		msgsnd(msg_id,(struct msgbuf_t*)&msg_snd,sizeof(msg_snd),0);
		msgrcv(msg_id2,(struct msgbuf_t*) &msg_rcv,sizeof(msg_rcv),prvi,0);
		printf("Sjeo posjetitelj %d\n ",pid);
		msgrcv(msg_id2,(struct msgbuf_t*) &msg_rcv,sizeof(msg_rcv),drugi,0);
		printf("Sisao posjetitelj %d\n ",pid);
					
	}
	printf("Zavrsio posjetitelj %d\n",pid);
		
}
void Vrtuljak(int pid,int msg_id,int msg_id2){
	sleep(2);
	struct msgbuf_t msg_rcv,msg_snd;
	int putnici[4];
	int brojPutnika = 0;
	srand(getpid());
	msgrcv(msg_id,(struct msgbuf_t*) &msg_rcv,sizeof(msg_rcv),0,0);
	printf("%s\n",msg_rcv.mtex);
	do{

		long z = msg_rcv.mtype;
		z+=8;
		msg_snd.mtype =z;
		strcpy(msg_snd.mtex,"Sjedni");

		msgsnd(msg_id2,(struct msgbuf_t*)&msg_snd,sizeof(msg_snd),0);
		putnici[brojPutnika]= z-8;
		brojPutnika++;
		if(brojPutnika==4){
			printf("Pokrenuo vrtuljak sa %d  %d  %d  %d\n",putnici[0],putnici[1],putnici[2],putnici[3]);
			int spat = rand()%2+1;
			sleep(spat);
			printf("Zaustavljen vrtuljak\n");
			strcpy(msg_snd.mtex,"Ustani");
			for(int i = 0;i<4;i++){
				msg_snd.mtype = putnici[i]+16;

				msgsnd(msg_id2,(struct msgbuf_t*)&msg_snd,sizeof(msg_snd),0);
			}
		
			brojPutnika = 0;
			
		}
		sleep(1);
					
		
	}while((msgrcv(msg_id,(struct msgbuf_t*) &msg_rcv,sizeof(msg_rcv),0,0)!=-1));
		

}
int main(void)
{
	
	
	int key = 384;
	int key2 = key+1;
	
	int glavniproces = getpid();
	int prvi=0;
	struct msgbuf_t msg_rcv,msg_snd;
	int msg_id;
	msg_id = msgget(key, 0600|IPC_CREAT);
	int msg_id2;
	msg_id2 = msgget(key2,0600|IPC_CREAT);
	for(int k = 0;k<8;k++){
		if(fork()==0){
			posjetitelj(k+1,msg_id,msg_id);
			return 0;
		}
			
	}
	
	if(getpid()==glavniproces){
		Vrtuljak(glavniproces,msg_id,msg_id);
	}
	msgctl(msg_id,IPC_RMID,NULL);

}

