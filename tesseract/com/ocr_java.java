package com;

public class ocr_java {
    static {
		System.loadLibrary("ocr_tesseract");
		//System.loadLibrary("ocr_java");
   }
	public native String OcrTesseract(String input, String output, String ocr_type);
	public static void main(String[] args) {
		String result = new ocr_java().OcrTesseract(args[1], args[2], "eng");
		System.out.println("result is "+result);
	}
}
