
    // linux 下读取大于2GB文件时，需指定  
    #define _FILE_OFFSET_BITS 64  
      
    #include <stdlib.h>  
    #include <stdio.h>  
    #include <errno.h>  
    #include <string.h>  
    #include <signal.h>
    #include <unistd.h>  
    #include <netdb.h>  
    #include <sys/socket.h>  
    #include <netinet/in.h>  
    #include <sys/types.h>  
    #include <arpa/inet.h>  
    #include <fcntl.h>
    #include <sys/wait.h>
    #include <iostream>
    #include<pthread.h>   
    //#include <opencv2/opencv.hpp>
    //#include <opencv2/highgui/highgui_c.h>
	#include "base64.h"
      
    // 定义包的大小为512KB  
    //#define PACK_SIZE 1024*512  

   // 定义包的大小为512KB  
    #define PACK_SIZE 1024*512  
void sig_child(int signo);

    int main(int argc, char *argv[])  
    {  
    pid_t pid;
    struct sigaction act;
        int sockfd,new_fd;  
        struct sockaddr_in server_addr;  
        struct sockaddr_in client_addr;  
        int sin_size,portnumber;   
    int i,n,m;
    memset(&act,0,sizeof(act));
    act.sa_handler = sig_child;

    if(sigaction(SIGCHLD,&act,0)){
        perror("Sigaction Error");
        return 1;
    }
      
        if((portnumber=atoi("8899"))<0)  
        {  
            exit(1);  
        }  
      
        /* 服务器端开始建立socket描述符 */  
        if((sockfd=socket(AF_INET,SOCK_STREAM,0))==-1) {  
            fprintf(stderr,"Socket error:%s\n\a",strerror(errno));  
            exit(1);  
        }  
      
        /* 服务器端填充 sockaddr结构  */  
        bzero(&server_addr,sizeof(struct sockaddr_in));  
        server_addr.sin_family=AF_INET;  
        server_addr.sin_addr.s_addr=htonl(INADDR_ANY);  
        server_addr.sin_port=htons(portnumber);  
      
        /* 捆绑sockfd描述符  */  
        if(bind(sockfd,(struct sockaddr *)(&server_addr),sizeof(struct sockaddr))==-1) {  
            fprintf(stderr,"Bind error:%s\n\a",strerror(errno));  
            exit(1);  
        }  
      
        //listen(socketfd,backlog)参数backlog 指定同时能处理的最大连接要求, 如果连接数目达此上限则client 端将收到ECONNREFUSED 的错误
        /* 监听sockfd描述符  */  
        if(listen(sockfd,5)==-1) {  
            fprintf(stderr,"Listen error:%s\n\a",strerror(errno));  
            exit(1);  
        }  

        while(1){

            fprintf(stderr, "server is listening!\n");

            /* 服务器阻塞,直到客户程序建立连接  */
            sin_size=sizeof(struct sockaddr_in);
            new_fd = accept(sockfd,(struct sockaddr *)(&client_addr),(socklen_t*)&sin_size );
            
            if(new_fd > 0) {
                    m = fork();
                    if(m == -1) {
                        perror("call to fork");
                        exit(1);
            } else if(m == 0) {
                fprintf(stderr,"Server get connection from %s\n", inet_ntoa(client_addr.sin_addr));
            int read_size = 0;
            unsigned long file_len  = 0;
            int order_id  = 0;
            char file_name[128] = "soc.txt";
            char file_info[PACK_SIZE] = {'\0'};
            char file_content[1024]={'\0'};
            char *file_tmp = NULL;
            std::string temp = "eof";

            // 读取指令
            printf("Waiting for read file info!\n");
            int nn = 0,i = 0,sn = 0;
            int wn = 0;
			//must end with \r\n , whether socket will be blocked
            //std::string  result = "2加3等于?";
            std::string  result = "continue\r\n";
            std::string result1 = "result:\r\n";
            const char* reDate= result.c_str();
            const char* reDate1= result1.c_str();
            
            // read_size is offset to store next recv data
            while((nn = read(new_fd, file_info+read_size, PACK_SIZE)) != -1){                
            	read_size += nn;
				printf("read_size = %d\n", read_size);
                printf("nn = %d\n", nn);
				//if((nn <= 0)&&(!(nn == EINTR || nn == EWOULDBLOCK || nn == EAGAIN)))
                if(nn < 8192) {
                	printf("send finish.\n");
					//do something to ocr detect
					std::string str64(file_info);
					std::string pstr;
					//std::cout<<str64<<std::endl;
                    {
                        /*此处添加识别， 并把识别结果放到reDate1尾部
                        实际输出内容为：result:识别结果\r\n 
                        (std::string result1 = "result:\r\n";) 默认的\r\n需要去掉
                        */
                    }
					//pstr = base64_decode(str64);
					//std::vector<char> data;
					//data.resize(pstr.size());
    				//data.assign(pstr.begin(),pstr.end());										
					//cv::Mat image = cv::imdecode(cv::Mat(data),1);
					//cv::imshow("img", image);
					//cv::waitKey(0);
					write(new_fd, reDate1, strlen(reDate));
                    break;
                }
				//must write back to socket, whether socket will be blocked. I don't know the reason
				write(new_fd, reDate, strlen(reDate));
            }
      
			//printf("%s ",file_info); 
         
            int sw = write(new_fd,reDate,strlen(reDate));
                
            std::cout<<"send to client:"<<result<<std::endl;

            if(sw ==-1) {
                   fprintf(stderr,"Write Error:%s\n",strerror(errno));
                   exit(1);
             }
    
            close(new_fd);
        exit(0);
            }
        }
        }

        close(sockfd);  
        exit(0);  

    
        return 0;


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
