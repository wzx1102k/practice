/bin/bash: 0: 未找到命令
一、如果只是命令行执行相关命令，不需要将其做为lib合到自己的程序里，只需更新如下执行档：
sudo apt-get install libjpeg62-dev  
sudo apt-get install libtiff4-dev  
sudo apt-get install zlib1g-dev 
sudo apt-get install libleptonica-dev
命令使用方式 在此不做更多介绍。

二、build tesseract lib 准备工作
1、下载tesseract src code （在git上找到一个开源的路径）
在本地创建一个tesseract目录，并下载
mkdir /home/cloud/tesseract
cd /home/cloud/tesseract
git clone https://github.com/tesseract-ocr/tesseract.git
git clone https://github.com/tesseract-ocr/langdata.git
git clone https://github.com/tesseract-ocr/tessdata.git
git clone https://github.com/tesseract-ocr/docs.git
git clone https://github.com/tesseract-ocr/tesseract-ocr.github.io.git

主要是前3个， 第1个是tesseract src code、2和3是训练字符库，其他是一些文档等。

2、由于tesseract 依赖 leptonica 库，所以还必须下载一包leptonica src code并编译生成leptonica lib, 不然会build fail.
root@yq-pc:/home/cloud# mkdir leptonica
root@yq-pc:/home/cloud# cd leptonica/
root@yq-pc:/home/cloud/leptonica# wget http://www.leptonica.org/source/leptonica-1.71.tar.gz 
看到如下信息 即下载完成：
Saving to: 'leptonica-1.71.tar.gz'

100%[======================================>] 10,212,309   452KB/s   in 84s    

2016-07-29 22:26:38 (118 KB/s) - 'leptonica-1.71.tar.gz' saved [10212309/10212309]

然后将压缩包解压到本地目录
root@yq-pc:/home/cloud/leptonica# tar -zxvf leptonica-1.71.tar.gz

三、编译leptonica 和 tesseract lib

1、编译leptonica 生成相应的lib
进入到解压后的目录 cd /home/cloud/leptonica/leptonica-1.71
执行如下命令
root@yq-pc:/home/cloud/leptonica/leptonica-1.71# ./configure
root@yq-pc:/home/cloud/leptonica/leptonica-1.71# make -j16

看到如下信息后 为编译完成
test -z "/usr/local/lib/pkgconfig" || /bin/mkdir -p "/usr/local/lib/pkgconfig"
 /usr/bin/install -c -m 644 lept.pc '/usr/local/lib/pkgconfig'
make[2]: Leaving directory `/home/cloud/leptonica/leptonica-1.71'
make[1]: Leaving directory `/home/cloud/leptonica/leptonica-1.71'

编译完之后会在如下路径下生成相应的lib，路径如果不知道是哪里，可以看编译时的提示信息
lib目录在：/usr/local/lib
root@yq-pc:/usr/local/lib# ls
liblept.a
liblept.la
liblept.so
liblept.so.4
liblept.so.4.0.2

头文件目录在： /usr/local/include
root@yq-pc:/usr/local/include# ls
leptonica

2、编译tesseract lib
进入到tesseracr目录 cd /home/cloud/tesseract/tesseract

设置环境变量 LIBLEPT_HEADERSDIR=/usr/local/include
root@yq-pc:/home/cloud/tesseract/tesseract# export LIBLEPT_HEADERSDIR=/usr/local/include

执行./configure
root@yq-pc:/home/cloud/tesseract/tesseract# ./configure --with-extra-libraries=/usr/local/lib

开始编译
root@yq-pc:/home/cloud/tesseract/tesseract# make install

如下信息为编译完成：
 /usr/bin/install -c -m 644 unicharambigs.5 unicharset.5 '/usr/local/share/man/man5'
make[2]: Leaving directory `/home/cloud/tesseract/tesseract/doc'
make[1]: Leaving directory `/home/cloud/tesseract/tesseract/doc'
root@yq-pc:/home/cloud/tesseract/tesseract# 

生成lib在/usr/local/lib下
root@yq-pc:/usr/local/lib# ls
libtesseract.a
libtesseract.la
libtesseract.so
libtesseract.so.3
libtesseract.so.3.0.4

生成头文件在/usr/local/include下
root@yq-pc:/usr/local/include# ls
leptonica  tesseract

四、tesseract程序调试

1、编写demo程序 和 makefile
具体demo程序 和 makefile 参看demo文件中相关内容

2、安装图片格式转换工具 ImageMagick
由于tesseract 输入文件为tif格式，需要将其他格式转换成tif。

root@yq-pc:/home/cloud/cloud-git-master/practice/tesseract# apt-get install ImageMagick

安装完后 执行convert xx.jpg xx.tif 即可完成转换
root@yq-pc:/home/cloud/cloud-git-master/practice/tesseract# convert ocr1.jpg ocr1.tif 

3、编译完生成可执行档，运行可执行档前需要设置环境变量指向字符训练库
在程序里api->Init(NULL, "eng") 则需要把路径指定到 eng.traineddata 所在位置
export TESSDATA_PREFIX=/home/cloud/tesseract/tessdata （这个就是前面所说git上下载的tessdata路径）

注： 如果有需要使用自己训练的字符库，则如下步骤：
<1>、找一个路径放置自己训练的字符库xx.traineddata
<2>、设置TESSDATA_PREFIX 路径指向它
<3>、程序里初始化时，指向该字符库名称 api->Init(NULL, "xx")

4、运行程序（这边写了一个auto_test.sh），直接运行查看效果：

root@yq-pc:/home/cloud/cloud-git-master/practice/tesseract# ls
auto_test.sh    Makefile  ocr1.tif  ocr2.tif  ocr3.tif    tesseract.cpp
demo_tesseract  ocr1.jpg  ocr2.jpg  ocr3.jpg  result.txt  tesseract.o
root@yq-pc:/home/cloud/cloud-git-master/practice/tesseract# ./auto_test.sh 
src_path: ocr1.tif
dec_path: result.txt
OCR output: 1098765443

.
src_path: ocr2.tif
dec_path: result.txt
OCR output: ” (33.2.5313-
5%?89
‘VUJKYZ
PQR8IL}
TKLﬁMﬂD

ARChﬁFmHT

.
src_path: ocr3.tif
dec_path: result.txt
OCR output: ABCIEFG
H I J KLMN
“PRST
UVWXYZ

运行完成后 结果保存在result.txt里，可以看到对于比较规范的图片 还是轻松识别的

五、程序里面调用ImageMagick 库

1、下载 ImageMagick src code

mkdir /home/cloud/imagemagick ; cd /home/cloud/imagemagick
root@yq-pc:/home/cloud/imagemagick# git clone http://git.imagemagick.org/repos/ImageMagick

2、编译ImageMagick lib

<1>配置
root@yq-pc:/home/cloud/imagemagick/ImageMagick# ./configure --disable-static --with-modules --without-perl --without-magick-plus-plus --with-quantum-depth=8

运行完成 提示：
    CXX             = g++
    CXXFLAGS        = -g -O2 -pthread
    FEATURES        = DPC HDRI Cipher OpenMP Modules
    DELEGATES       = mpeg fontconfig freetype jbig jng jpeg lzma pango png ps tiff x zlib
==============================================================================

<2> 编译
root@yq-pc:/home/cloud/imagemagick/ImageMagick# make -j16

运行完提示：
  CCLD     coders/svg.la
  CCLD     utilities/magick
make[1]:正在离开目录 `/home/cloud/imagemagick/ImageMagick'

<3> 生成lib
root@yq-pc:/home/cloud/imagemagick/ImageMagick# make install
运行完提示：
/usr/bin/install -c -m 644 MagickCore/ImageMagick.pc MagickCore/MagickCore.pc MagickCore/ImageMagick-7.Q8HDRI.pc MagickCore/MagickCore-7.Q8HDRI.pc MagickWand/MagickWand.pc MagickWand/MagickWand-7.Q8HDRI.pc '/usr/local/lib/pkgconfig'
make[2]:正在离开目录 `/home/cloud/imagemagick/ImageMagick'
make[1]:正在离开目录 `/home/cloud/imagemagick/ImageMagick'

<4> 在/usr/local/lib 和 /usr/local/include 下 可以查看到 lib 和头文件
root@yq-pc:/usr/local/lib# ls
ImageMagick-7.0.2
libMagickCore-7.Q8HDRI.la
libMagickCore-7.Q8HDRI.so
libMagickCore-7.Q8HDRI.so.0
libMagickCore-7.Q8HDRI.so.0.0.0

root@yq-pc:/usr/local/include# ls
ImageMagick-7  leptonica  tesseract


注： 如果执行ImageMagick 命令提示找不到so:
root@yq-pc:/home/cloud/cloud-git-master/practice/tesseract# import ocr1.png 
import: error while loading shared libraries: libMagickCore-7.Q8HDRI.so.0: cannot open shared object file: No such file or directory
可执行ldconfig /usr/local/lib/  再运行命令即可成功
ImageMagick 是一个很强大的图像编辑工具，图像格式转换、图像旋转、图像截取、图像加燥去燥、 图像二值化等等，具体参看如下链接。
截取图像：
执行 import ocr1.png 此时鼠标会变成四角光标，拖出一片区域并释放，则保存该区域图像到ocr1.png中。（和QQ截图操作一样）
查看图片 display ocr1.png 即可看到之前截图的图片



相关参考：
http://www.eefocus.com/winter1988/blog/13-03/292209_03d5b.html
http://stackoverflow.com/questions/14951784/how-to-force-tesseract-not-to-use-tessdata-prefix
http://www.cnblogs.com/cappuccino/p/4650665.html
http://san-yun.iteye.com/blog/1954866
http://www.linuxidc.com/Linux/2011-07/38728.htm
https://github.com/tesseract-ocr
http://git.imagemagick.org/repos/ImageMagick/tree/master/ImageMagick
http://rmagick.rubyforge.org/install-linux.html
http://blog.csdn.net/dj0379/article/details/7527955
http://www.imagemagick.org/discourse-server/viewtopic.php?t=17059

imagemagick推荐看这篇
http://www.charry.org/docs/linux/ImageMagick/ImageMagick.html
http://www.imagemagick.org/script/magick-core.php
http://www.imagemagick.org/script/magick-wand.php
http://blog.csdn.net/leixiaohua1020/article/details/26754089
http://www.ibm.com/developerworks/cn/opensource/os-imagemagick/
http://www.imagemagick.org/api/constitute.php
http://www.cnblogs.com/jamesmile/archive/2010/10/19/1855469.html
http://stackoverflow.com/questions/17562135/declaration-of-c-function-void-msgboxconst-char-const-char-conflicts-with

jbig lib download
https://launchpad.net/ubuntu/+source/jbigkit/2.1-3.1
bio.gsi.de/DOCS/SOFTWARE/libjbig.html

static & dynamic lib
http://www.cnblogs.com/chengxuyuancc/archive/2013/05/11/3072981.html
http://blog.chinaunix.net/uid-23069658-id-3142046.html
http://blog.csdn.net/dream_it_life/article/details/8598616
http://stackoverflow.com/questions/19768267/relocation-r-x86-64-32s-against-linking-error






