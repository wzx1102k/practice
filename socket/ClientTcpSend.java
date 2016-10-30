    import java.io.DataOutputStream;
    import java.io.File;
    import java.io.FileInputStream;
    import java.net.InetSocketAddress;
    import java.net.Socket;

// ip port filepath
    public class ClientTcpSend {
        public static void main(String[] args) {
            int length = 0;
            byte[] sendBytes = null;
            Socket socket = null;
            DataOutputStream dos = null;
            FileInputStream fis = null;

            try {
                try {
                    socket = new Socket();
                    socket.connect(new InetSocketAddress(args[0], Integer.parseInt(args[1])),
                                   10 * 1000);
                    dos = new DataOutputStream(socket.getOutputStream());
                    File file = new File(args[2]);
                    fis = new FileInputStream(file);
                    sendBytes = new byte[1024];
                    while ((length = fis.read(sendBytes, 0, sendBytes.length)) > 0) {
                        dos.write(sendBytes, 0, length);
                        dos.flush();
                    }
                } finally {
                    if (dos != null)
                        dos.close();
                    if (fis != null)
                        fis.close();
                    if (socket != null)
                        socket.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
