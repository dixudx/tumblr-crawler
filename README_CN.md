tumblr-crawler
===============

这是一个[Python](https://www.python.org)的脚本,配置运行后可以从某些你指定的tumblr博客
下载图片和视频.

## 环境安装

#### 程序猿和程序媛见这里

配置好你的Python环境,然后`pip install requests xmltodict`.

或者

```bash
$ git clone https://github.com/dixudx/tumblr-crawler.git
$ cd tumblr-crawler
$ pip install -r requirements.txt
```

大功告成,直接跳到下一节配置和运行.

#### 小白见这里

1. 首先你需要一个Python的环境,安装方法请
参照[这里](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001374738150500472fd5785c194ebea336061163a8a974000).

2. 安装`pip`(主要是希望通过`pip`来安装Python的一些依赖包)

    * 当然也可以通过其他方式来安装这些包(此处自行百度),推荐通过`pip`来安装依赖包;
    * 如果你是Windows用户,按照上面第一个步骤来安装的Python,那么请忽略这一步,
    因为已经安装过了; 如果忘记勾选,安装教程见[这里](http://www.tuicool.com/articles/eiM3Er3/)
    * Mac用户,请参照[这个教程](http://blog.csdn.net/fancylovejava/article/details/39140373)

3. 下载[tumblr-crawler](https://github.com/dixudx/tumblr-crawler/archive/master.zip)并解压缩;


## 配置和运行

有两种方式来指定你要下载的站点,一是编辑sites.txt,二是指定命令行参数.

### 第一种方法:编辑sites.txt文件

找到一个文字编辑器,然后打开文件`sites.txt`,把你想要下载的Tumblr站点编辑进去,以逗号分隔,不要有空格,不需要`.tumblr.com`的后缀.例如,如果你要下载_vogue.tumblr.com_ and _gucci.tumblr.com_,这个文件看起来是这样的:

```
vogue,gucci
```

然后保存文件,双击运行`tumblr-photo-video-ripper.py`或者在终端(terminal)里面
运行`python tumblr-photo-video-ripper.py`

### 第二种方法:使用命令行参数(仅针对会使用操作系统终端的用户)

如果你对Windows或者Unix系统的命令行很熟悉,你可以通过指定运行时的命令行参数来指定要下载的站点:

```bash
python tumblr-photo-video-ripper.py site1,site2
```

站点的名字以逗号分隔,不要有空格,不需要`.tumblr.com`的后缀.

### 站点图片/视频的下载与保存

程序运行后,会默认在当前路径下面生成一个跟tumblr博客名字相同的文件夹,
照片和视频都会放在这个文件夹下面.

运行这个脚本,不会重复下载已经下载过的图片和视频,所以不用担心重复下载的问题.同时,多次运行可以
帮你找回丢失的或者删除的图片和视频.
