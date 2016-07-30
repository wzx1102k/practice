JNI调用demo步骤：

step 1.设置JAVA环境(具体依据个人电脑安装的jdk toolchain路径)
export JAVA_HOME=/tools/jdk1.6.0_38
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar  (第一个点表示当前路径，因为demo里生成的class在当前目录)
export PATH=$PATH:$JAVA_HOME/bin

step 2.编译hello java例程(javac执行完生成了hello class,必须保证文件名称和里面包含的类名称一致)
cloud.yu@tc-002:~/linux_test/java$ javac com/hello.java 
cloud.yu@tc-002:~/linux_test/java/com$ ls
hello.class  hello.java

step 3.生成JNI可调用头文件(javah -jni可生成， com.hello表示com文件夹下的com/hello)
cloud.yu@tc-002:~/linux_test/java$ javah -jni com.hello
cloud.yu@tc-002:~/linux_test/java$ ls
com           com_hello.h

step 4. 编写hello.cpp，在其中include com_hello.h，编写makefile
头文件中的Java_com_magc_jni_HelloWorld_DisplayHello(JNIEnv *, jobject)方法，是将来与动态链接库交互的接口，并需要和C++程序名字保持一致

step 5. 编译生成libhello.so 
(makefile里生成的.so一定要以lib头来命名，java编译和makefile一样会去找lib字样)
libhello.so名称一定要和java里System.loadLibrary("hello");名称一致。
比如是libOpencv.so，那java里就是System.loadLibrary("Opencv")，区分大小写
cloud.yu@tc-002:~/linux_test/java$ make
g++ -c -fPIC -I /tools/jdk1.6.0_38/include -I /tools/jdk1.6.0_38/include/linux hello.cpp
g++ -shared -fPIC -o libhello.so hello.o
cloud.yu@tc-002:~/linux_test/java$ ls
com  com_hello.h  hello.cpp  hello.o  libhello.so  Makefile  readme.txt

step 6. 执行java程序，调用c++函数
cloud.yu@tc-002:~/linux_test/java$ java -Djava.library.path=. com.hello
From jni_helloworldImpl.cpp :Hello world !
执行成功

step7. jni多文件调用，只需JNI定义需要的接口
在hello中我调用了thread_test.cpp中的test函数，而这个函数又依赖于系统的thread lib，但是我不需要在jni里定义这些接口。
重新编译后 执行结果如下：
cloud.yu@tc-002:~/linux_test/java$ java -Djava.library.path=. com.hello
From jni_helloworldImpl.cpp :Hello world ! 
main thread pid is 2924
child thread pid is 2924
count = 9
count = 8
count = 7
count = 6
count = 5
count = 4
count = 3
count = 2
count = 1
count = 0
可见可以正常使用。

