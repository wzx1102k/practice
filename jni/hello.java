package com;

public class hello {
    static {
        System.loadLibrary("hello");
   }
    public     native void DisplayHello();
		public static void main(String[] args) {
        new hello().DisplayHello();
	}
}
