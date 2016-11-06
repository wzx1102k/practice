import java.io.*;   
import java.net.*;  
import java.util.*; 
import java.lang.Integer; 

// java MyServer port
//java MyServer 45536
public class MyServer {   
    public static void main(String[] args) throws IOException{   
        ServerSocket server=new ServerSocket(Integer.parseInt(args[0]));   
        while(true){  
        Socket client=server.accept();  
        BufferedReader in=new BufferedReader(new InputStreamReader(client.getInputStream()));   
            String str=in.readLine();   
            System.out.println(str);    
        client.close();  
        }   
    }   
}  
