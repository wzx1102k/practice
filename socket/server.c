
    /******** http://blog.csdn.net/robertkun ********/  
    /*******  服务器程序  (server.c)     ************/  
      
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
    #include <fcntl.h>  
      
    // 定义包的大小为512KB  
    #define PACK_SIZE 1024*512  
      
    int main(int argc, char *argv[])  
    {  
        // 设置输出缓冲  
        setvbuf(stdout, NULL, _IONBF, 0);  
        fflush(stdout);  
      
        int sockfd,new_fd;  
        struct sockaddr_in server_addr;  
        struct sockaddr_in client_addr;  
        int sin_size,portnumber;  
        char hello[]="Hello! Are You Fine?\n";  
      
        if((portnumber=atoi(argv[1]))<0)  
        {  
            fprintf(stderr,"Usage:%s portnumber\a\n",argv[1]);  
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
      
        /* 监听sockfd描述符  */  
        if(listen(sockfd,5)==-1) {  
            fprintf(stderr,"Listen error:%s\n\a",strerror(errno));  
            exit(1);  
        }  
      
        while(1)  
        {  
            fprintf(stderr, "server is listening!\n");  
      
            /* 服务器阻塞,直到客户程序建立连接  */  
            sin_size=sizeof(struct sockaddr_in);  
            if( ( new_fd = accept(sockfd,(struct sockaddr *)(&client_addr),(socklen_t*)&sin_size ) ) == -1) {  
                fprintf(stderr,"Accept error:%s\n\a",strerror(errno));  
                exit(1);  
            }  
      
            fprintf(stderr,"Server get connection from %s\n",  
                inet_ntoa(client_addr.sin_addr));  
            if(write(new_fd,hello,strlen(hello))==-1) {  
                fprintf(stderr,"Write Error:%s\n",strerror(errno));  
                exit(1);  
            }  
      
            long int read_size = 0;  
            unsigned long file_len  = 0;  
            int order_id  = 0;  
            char file_name[128] = {'\0'};  
            char file_info[1024] = {'\0'};  
      
            // 读取指令  
            printf("\n\nWaiting for read file info!\n");  
            int nn = 0;  
            if(nn = read(new_fd, file_info, 1024))   
            {  
                // 指令ID  
                int id_h = (int)file_info[0]<<8;  
                order_id = id_h + (int)file_info[1];  
      
                // 文件长度  
                // 高16位  
                unsigned long len_hig_1 = 0;  
                memcpy(&len_hig_1, &file_info[2], sizeof(file_info[2]));  
      
                unsigned long len_hig_2 = 0;  
                memcpy(&len_hig_2, &file_info[3], sizeof(file_info[3]));  
      
                unsigned long len_hig = len_hig_1 * 256 + len_hig_2;  
      
                // 低16位  
                unsigned long len_low_1 = 0;  
                memcpy(&len_low_1, &file_info[4], sizeof(file_info[4]));  
      
                unsigned long len_low_2 = 0;  
                memcpy(&len_low_2, &file_info[5], sizeof(file_info[5]));  
      
                int len_low = len_low_1 * 256 + len_low_2;  
                file_len = len_hig * 256 * 256 + len_low;  
      
                // 文件名称  
                strncpy(file_name, &file_info[6], strlen(&file_info[6]));  
      
                printf("order = %d, %lu, %s\n", order_id, file_len, file_name);  
      
                if((strlen(file_name) == 0) || (file_len == 0))  
                {  
                    printf("Read file info error!\n File_name or file_len is zero!\n");  
                    close(new_fd);  
                    continue;  
                }  
            }  
            else {  
                printf("Read file info error!\n");  
                close(new_fd);  
                close(sockfd);  
                exit(0);  
            }  
      
            // 写入文件  
            printf("\n\nWaiting for read file content!\n");  
            FILE* pf = fopen(file_name, "wb+");  
            if(pf == NULL)  
            {  
                printf("Open file error!\n");  
                close(new_fd);  
                continue;  
            }  
      
            char buff[PACK_SIZE] = {'\0'};  
            while(read_size <= file_len) {  
                //bzero(buff, 1024);  
                int rlen = read(new_fd, buff, PACK_SIZE);  
                if(rlen) {  
                    //system("clear");  
                    printf("\n\nRead package size = %d\n", rlen);  
      
                    int wn = fwrite(buff, sizeof(char), rlen, pf);  
                    read_size += rlen;  
      
                    printf("write file size = %d\n", wn);  
                    //printf("Read  total  size = %d\n", read_size);  
                }  
                else {  
                    printf("Read over!...%d\n", rlen);  
                    break;  
                }  
            } // End While  
      
            printf("File len = %ld ... Already read size = %ld\n", file_len, read_size);  
          
            /* 这个通讯已经结束     */  
            fclose(pf);  
            close(new_fd);  
            /* 循环下一个     */  
        }  
      
        close(sockfd);  
        exit(0);  
    }  

