/* server.c */
#include <opencv/cv.hpp>
#include <opencv/highgui.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <netinet/in.h>
#include<errno.h>   
#include<netdb.h>   
#include<sys/socket.h>   
#include<pthread.h>   
#include<fcntl.h>  
#include <arpa/inet.h>  // inet_ntoa
#include "base64.h"
#include <iostream>
//#include "wrap.h"

#define RCVLINE 4*1024
#define MAXLINE 512*1024 //512K
#define SERV_PORT 9000

using namespace std;

void sig_child(int signo);

int main(void)
{
        pid_t pid;
        struct sigaction act;
        struct sockaddr_in servaddr,cliaddr;
        socklen_t cliaddr_len;
        int listenfd,connfd;
        char buf[RCVLINE] = "good luck!!\r\n";
        char str[INET_ADDRSTRLEN];
        int i,n,m;
        
        memset(&act,0,sizeof(act));
        act.sa_handler = sig_child;
        
        if(sigaction(SIGCHLD,&act,0)){
                perror("Sigaction Error");
                return 1;
        }
        
        listenfd = socket(AF_INET,SOCK_STREAM,0);
        bzero(&servaddr,sizeof(servaddr));
        servaddr.sin_family = AF_INET;
        servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
        servaddr.sin_port = htons(SERV_PORT);
        
        bind(listenfd,(struct sockaddr *)&servaddr,sizeof(servaddr));
        
        listen(listenfd,20);
        
        printf("Accepting connections ...\n");
        
        while(1)
        {
                cliaddr_len = sizeof(cliaddr);
                connfd = accept(listenfd,(struct sockaddr *)&cliaddr,&cliaddr_len);
                printf("connfd=%d\n", connfd);
				if(connfd > 0)
				{
					m = fork();
					if(m == -1)
					{
                        perror("call to fork");
                        exit(1);
					}
					else if(m == 0)
					{
						char subbuf[MAXLINE];
						char rcvbuf[RCVLINE];
						char substr[INET_ADDRSTRLEN];
						int count = 0;
						printf("fork \n");
						while(1)
							{
								printf("start to recv\n");
                                ssize_t serrno = recv(connfd, subbuf+count,MAXLINE,0);
                                printf("serrno = %ld\n", serrno); 
								if((serrno <= 0)&&(!(serrno == EINTR || serrno == EWOULDBLOCK || serrno == EAGAIN))){
                                        printf("the other side has been closed.\n");
										std::string str64(subbuf);
										std::string pstr;
										std::cout<<str64<<std::endl;
										pstr = base64_decode(str64);
										vector<char> data;
										data.resize(pstr.size());
    									data.assign(pstr.begin(),pstr.end());										
										//std::cout<< pstr << std::endl;
										cv::Mat image = cv::imdecode(cv::Mat(data),1);
										//printf("content %s",subbuf);
                                		//write(connfd, buf, RCVLINE);
										cv::imshow("img", image);
										cv::waitKey(0);
										write(connfd, buf, RCVLINE);
                                        break;
                                }
								inet_ntop(AF_INET,&cliaddr.sin_addr,substr,sizeof(substr));
								printf("%d: received from %s at PORT %d\n",count, substr,ntohs(cliaddr.sin_port));
								count += serrno ;
								write(connfd, buf, RCVLINE);
							}
                        
                        close(connfd);
                        exit(0);
                }
                else
                {
                        close(connfd);
                }
			}
        }
}

// SIGCHLD handler
void sig_child(int signo)
{
        pid_t pid;
        int stat;
        
        while((pid = waitpid(-1,&stat,WNOHANG)) > 0)
        {
                printf("chile %d terminated\n",pid);
        }
        
        return;
}
