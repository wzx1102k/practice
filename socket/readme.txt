一共有5个shell脚本：

测试例子中JAVA SERVER 使用33456 端口， C SERVER使用8080 端口

<1> auto_c_client.sh 执行 c的client程序， 用于发送图片1.png 给相应的端口
<2> auto_c_server.sh 执行c的server程序，用于监听8080端口，并接收数据
<3> auto_java_client.sh 执行java的client程序， 发送图片给相应端口
<4> auto_java_server.sh 执行java的server程序，用于监听33456端口，并接收
<5> auto_java_release.sh  修改java程序后执行它 重新生成java class

测试时，打开两个终端， 一个用于server 监听， 一个用于client 发送

脚本里的端口号client 和server必须匹配

测试完必须ctrl+c 退出 关闭对端口的占用， 异常退出会占用端口 导致下次调用无效。

如提示端口被占用， 可以使用ps -aux 查看有哪些进程， 看 执行的./auto_java_xx 或者./auto_c_xx 脚本 是否还活着， 
如果活着从第一行读取它的PID值，通过 kill -s 9 PID值 结束该程序， 再运行 就不会提示被占用里。

目前测试结果 c client 和 c server之间 传输正常； java client 和 java server之间也正常

c client 发给 java server 或者 java client 发给 c server 不正常， 提示有监听到数据，接收时会卡住， 目前看起来可能是java 和 c 的报文格式不一致导致，需要进一步查看。

