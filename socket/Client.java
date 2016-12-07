/****************** Client program *****************/
import java.net.*;
import java.io.*;

public class Client {
    static Socket server;

    private final static char[] ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".toCharArray();

    private static int[]  toInt   = new int[128];

    static {
        for(int i=0; i< ALPHABET.length; i++){
            toInt[ALPHABET[i]]= i;
        }
    }

    /**
     * Translates the specified byte array into Base64 string.
     *
     * @param buf the byte array (not null)
     * @return the translated Base64 string (not null)
     */
    public static String encode(byte[] buf){
        int size = buf.length;
        char[] ar = new char[((size + 2) / 3) * 4];
        int a = 0;
        int i=0;
        while(i < size){
            byte b0 = buf[i++];
            byte b1 = (i < size) ? buf[i++] : 0;
            byte b2 = (i < size) ? buf[i++] : 0;

            int mask = 0x3F;
            ar[a++] = ALPHABET[(b0 >> 2) & mask];
            ar[a++] = ALPHABET[((b0 << 4) | ((b1 & 0xFF) >> 4)) & mask];
            ar[a++] = ALPHABET[((b1 << 2) | ((b2 & 0xFF) >> 6)) & mask];
            ar[a++] = ALPHABET[b2 & mask];
        }
        switch(size % 3){
            case 1: ar[--a]  = '=';
            case 2: ar[--a]  = '=';
        }
        return new String(ar);
    }

    /**
     * Translates the specified Base64 string into a byte array.
     *
     * @param s the Base64 string (not null)
     * @return the byte array (not null)
     */
    public static byte[] decode(String s){
        int delta = s.endsWith( "==" ) ? 2 : s.endsWith( "=" ) ? 1 : 0;
        byte[] buffer = new byte[s.length()*3/4 - delta];
        int mask = 0xFF;
        int index = 0;
        for(int i=0; i< s.length(); i+=4){
            int c0 = toInt[s.charAt( i )];
            int c1 = toInt[s.charAt( i + 1)];
            buffer[index++]= (byte)(((c0 << 2) | (c1 >> 4)) & mask);
            if(index >= buffer.length){
                return buffer;
            }
            int c2 = toInt[s.charAt( i + 2)];
            buffer[index++]= (byte)(((c1 << 4) | (c2 >> 2)) & mask);
            if(index >= buffer.length){
                return buffer;
            }
            int c3 = toInt[s.charAt( i + 3 )];
            buffer[index++]= (byte)(((c2 << 6) | c3) & mask);
        }
        return buffer;
    } 

    //图片转化成base64字符串
    public static String GetImageStr(String imgPath)  
    {//将图片文件转化为字节数组字符串，并对其进行Base64编码处理  
        String imgFile = imgPath;//待处理的图片  
        InputStream in = null;  
        byte[] data = null;  
        //读取图片字节数组  
        try   
        {  
            in = new FileInputStream(imgFile);          
            data = new byte[in.available()];  
            in.read(data);  
            in.close();  
        }   
        catch (IOException e)   
        {  
            e.printStackTrace();  
        }  
        //对字节数组Base64编码  
        return encode(data);//返回Base64编码过的字节数组字符串  
    }  
      
    //base64字符串转化成图片  
    public static boolean GenerateImage(String imgStr, String imgPath)  
    {   //对字节数组字符串进行Base64解码并生成图片  
        if (imgStr == null) //图像数据为空  
            return false;  
        try   
        {  
            //Base64解码  
            byte[] b = decode(imgStr);  

            //生成jpeg图片  
            String imgFilePath = imgPath;//新生成的图片  
            OutputStream out = new FileOutputStream(imgFilePath);      
            out.write(b);  
            out.flush();  
            out.close();  
            return true;  
        }
        catch (Exception e)   
        {  
            return false;  
        }  
    }

    public static void main(String[] args) throws Exception {
        server = new Socket("127.0.0.1", 8899);
        BufferedReader rcv01 = new BufferedReader(new InputStreamReader(server.getInputStream()));
        String img64 = GetImageStr(args[0]);
        long fileLength = img64.length();
       String header = "Image_length:" + String.valueOf(fileLength) + "?";
       // String body = header + img64;
        String body = img64;
		//System.out.println(header);
        //System.out.println(img64);
        PrintWriter send01 = new PrintWriter(server.getOutputStream());
        //屏幕输入 叫做System.in
        //BufferedReader wt = new BufferedReader(new InputStreamReader(System.in));

        //String str = wt.readLine();
        send01.println(body);
        send01.flush();
        while (true) {
            String str_rcv = rcv01.readLine();
            System.out.println("服务器:"+str_rcv);
            if(str_rcv.contains("result:")) {
                //拿到识别结果保存，同时结束此次socket
                System.out.println("start to close "+str_rcv);
            	break;
            }
        }
        server.close();
    }
}
