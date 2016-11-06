    </pre><pre code_snippet_id="1784587" snippet_file_name="blog_20160726_1_6356653" name="code" class="cpp">
    #include <stdio.h>  
    #include <string.h>  
    #include <sys/socket.h>  
    #include <arpa/inet.h>  
    #include <unistd.h>  
    #include <netinet/in.h>  
    #include <stdlib.h>  
      
    #define MAXLINE 1024  
      
    int post(char *ip,int port,char *page,char *msg){  
        int sockfd,n;  
        char recvline[MAXLINE];  
        struct sockaddr_in servaddr;  
        char content[4096];  
        char content_page[50];  
        sprintf(content_page,"POST /%s HTTP/1.1\r\n",page);  
        char content_host[50];  
        sprintf(content_host,"HOST: %s:%d\r\n",ip,port);  
        char content_type[] = "Content-Type: application/x-www-form-urlencoded\r\n";  
        char content_len[50];  
        sprintf(content_len,"Content-Length: %d\r\n\r\n",strlen(msg));  
        sprintf(content,"%s%s%s%s%s",content_page,content_host,content_type,content_len,msg);  
        if((sockfd = socket(AF_INET,SOCK_STREAM,0)) < 0)  
            printf("socket error\n");  
        bzero(&servaddr,sizeof(servaddr));  
        servaddr.sin_family = AF_INET;  
        servaddr.sin_port = htons(80);  
        if(inet_pton(AF_INET,ip,&servaddr.sin_addr) <= 0)  
            printf("inet_pton error\n");  
        if(connect(sockfd,(struct sockaddr *)&servaddr,sizeof(servaddr)) < 0)  
            printf("connect error\n");  
        write(sockfd,content,strlen(content));  
        while((n = read(sockfd,recvline,MAXLINE)) > 0)  
        {  
            recvline[n] = 0;  
            if(fputs(recvline,stdout) == EOF)  
                printf("fputs error\n");  
        }  
        if(n < 0)  
            printf("read error\n");  
      
    }  
      
    int main()  
    {  
        char msg[] = "name=A&id=1";  
        char ip[] = "127.0.0.1";  
        int port = 33456;  
        char page[] = "xxxx.do";  
        post(ip,80,page,msg);  
        exit(0);  
    }  
