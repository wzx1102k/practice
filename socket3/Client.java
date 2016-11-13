/****************** Client program *****************/
import java.net.*;
import java.io.*;

public class Client {
static Socket server;

public static void main(String[] args) throws Exception {
   //server = new Socket(InetAddress.getLocalHost(), 5678);
   server = new Socket("127.0.0.1", 9000);
	BufferedReader rcv01 = new BufferedReader(new InputStreamReader(server.getInputStream()));
   PrintWriter send01 = new PrintWriter(server.getOutputStream());
   //屏幕输入 叫做System.in
   BufferedReader wt = new BufferedReader(new InputStreamReader(System.in));

   while (true) {
    String str = wt.readLine();
	send01.println(str);
    send01.flush();
    String str_rcv = rcv01.readLine();
	System.out.println("服务器:"+str_rcv);

	if (str.equals("end")) {
     break;
    }
   }
   server.close();
}
}
