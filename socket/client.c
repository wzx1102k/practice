
    /******** http://blog.csdn.net/robertkun ********/  
    /******* 客户端程序  client.c        ************/  
      
    // linux 下读取大于2GB文件时，需指定  
    #define _FILE_OFFSET_BITS 64  
      
    #include <stdlib.h>  
    #include <stdio.h>  
    #include <errno.h>  
    #include <string.h>  
    #include <unistd.h>  
    #include <netdb.h>  
    #include <sys/socket.h>  
    #include <netinet/in.h>  
    #include <sys/types.h>  
    #include <arpa/inet.h>  
    #include <sys/stat.h>  
    #include <fcntl.h>    // 文件读写  
      
    // 定义包的大小为512KB  
    #define PACK_SIZE 1024*512  
      
    char* get_file_name(char* fn);  
    unsigned long get_file_size(const char *path);  
      
    int main(int argc, char *argv[])  
    {  
        if(argc < 2)  
        {  
            printf("please input:<ip> <port> <filePath>.\n");  
            return 0;  
        }  
      
            // 设置输出缓冲  
            setvbuf(stdout, NULL, _IONBF, 0);  
            fflush(stdout);  
      
        char* filePath = argv[3];  
        if(access(filePath, F_OK) != 0)  
        {  
            printf("file not existed!\n");  
            return 0;  
        }  
      
            int sockfd;  
            char buff[1024] = {'\0'};  
            struct sockaddr_in server_addr;  
            struct hostent *host;  
            int portnumber,nbytes;  
      
        const char* ip = argv[1];  
            if((host=gethostbyname(ip))==NULL)  
            {  
                    fprintf(stderr,"Gethostname error\n");  
                    exit(1);  
            }  
      
        const char* port = argv[2];  
            if((portnumber=atoi(port))<0)  
            {  
                    fprintf(stderr,"Usage:%s hostname portnumber\a\n",argv[0]);  
                    exit(1);  
            }  
      
            /* 客户程序开始建立 sockfd描述符  */  
            if((sockfd=socket(AF_INET,SOCK_STREAM,0))==-1)  
            {  
                    fprintf(stderr,"Socket Error:%s\a\n",strerror(errno));  
                    exit(1);  
            }  
      
            /* 客户程序填充服务端的资料       */  
            bzero(&server_addr,sizeof(server_addr));  
            server_addr.sin_family=AF_INET;  
            server_addr.sin_port=htons(portnumber);  
            server_addr.sin_addr=*((struct in_addr *)host->h_addr);  
      
            /* 客户程序发起连接请求         */  
            if(connect(sockfd,(struct sockaddr *)(&server_addr),sizeof(struct sockaddr))==-1)  
            {  
                    fprintf(stderr,"Connect Error:%s\a\n",strerror(errno));  
                    exit(1);  
            }  
      
            /* 连接成功了           */  
            if((nbytes=read(sockfd,buff,1024))==-1)  
            {  
                    fprintf(stderr,"Read Error:%s\n",strerror(errno));  
                    exit(1);  
            }  
            buff[nbytes]='\0';  
            printf("I have received:%s\n",buff);  
      
        /******* 发送指令 ********/  
        bzero(buff,1024);  
        // 指令ID  
        int order = 0x0010;  
        int order_h = order >> 8;  
        buff[0] = (char)order_h;  
        buff[1] = (char)order;  
      
        // 文件长度  
        unsigned long len = get_file_size(filePath);  
        printf("file size = %lu\n", len);  
      
        // 高16位  
        int len_h = len >> 16;  
        int len_h_1 = len_h >> 8;  
        buff[2] = (char)len_h_1;  
        buff[3] = (char)len_h;  
      
        // 低16位  
        int len_l = len;  
        int len_l_1 = len_l >> 8;  
        buff[4] = (char)len_l_1;  
        buff[5] = (char)len_l;  
      
        // 文件名称  
        char* fileName = get_file_name(filePath);  
        printf("file name = %s\n", fileName);  
        strncpy(&buff[6], fileName, strlen(fileName));  
      
        write(sockfd,buff,1024);      
          
        /******* 发送文件 ********/  
        printf("file path = %s\n", filePath);  
        FILE* pf = fopen(filePath, "rb");  
        if(pf == NULL) {  
            printf("open file failed!\n");  
            exit(0);  
        }  
      
        char pack[PACK_SIZE] = {'\0'};  
        while((len = fread(pack, sizeof(char), PACK_SIZE, pf)) > 0)  
            {  
            system("clear");  
            printf("send data size = %ld \t", len);  
            write(sockfd, pack, len);  
            bzero(pack,PACK_SIZE);  
            //sleep(1);  
            }  
          
            /* 结束通讯     */  
            close(sockfd);  
            exit(0);  
    }  
      
    char* get_file_name(char* fn)  
    {  
        int last = 0;  
        char* pfn = fn+strlen(fn)-1;  
        int i=0;  
        for(i=0; i<strlen(fn); ++i)  
        {  
            if(*pfn-- == '/')  
            {  
                last = strlen(fn)-i;  
                break;  
            }  
        }  
      
        char* name = (char*)malloc(sizeof(char)*256);  
        char* pname = name;  
        int j=0;  
        for(j=last; j<strlen(fn); ++j, ++pname)  
        {  
            *pname = fn[j];  
        }  
          
        return name;  
    }  
      
    unsigned long get_file_size(const char *path)  
    {  
        unsigned int filesize = 0;  
        struct stat statbuff;  
        if(stat(path, &statbuff) < 0) {  
            printf("Get file stat failed!\n");  
            return filesize;  
        }else{  
            filesize = statbuff.st_size;  
        }  
      
        return filesize;  
    }  

