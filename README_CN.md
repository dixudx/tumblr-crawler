tumblr-crawler
===============

这是一个[Python](https://www.python.org)的脚本,配置运行后可以从某些你指定的tumblr博客
下载图片和视频.

## 怎么样方便地讨论交流

* 我们现在有了[Slack](https://join.slack.com/t/tumblr-crawler/shared_invite/enQtMzM0MTM1MzkwMDM0LTY0OTg2ZTk0MGI5NTU4NDRlYjc4ZDM3OWIxYmE2ZWJhMTdkZmQxYmM0ZWVhYWJmMjM3MTkwMTkxMTQwYTk4ZDk), 欢迎大家加入, 讨论并解决问题.
* 或者直接在[Github](https://github.com/dixudx/tumblr-crawler/issues/new)上开新的issue;

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
    * 然后在终端(terminal)里面运行 `pip install xmltodict six "requests>=2.10.0" "PySocks>=1.5.6"`;


3. 下载[tumblr-crawler](https://github.com/dixudx/tumblr-crawler/archive/master.zip)并解压缩;


## 配置和运行

有两种方式来指定你要下载的站点,一是编辑`sites.txt`,二是指定命令行参数.

### 第一种方法:编辑sites.txt文件

找到一个文字编辑器,然后打开文件`sites.txt`,把你想要下载的Tumblr站点编辑进去,以逗号/空格/tab/表格鍵/回车符分隔,可以多行,不需要`.tumblr.com`的后缀.例如,如果你要下载 _vogue.tumblr.com_ and _gucci.tumblr.com_,这个文件看起来是这样的:

```
vogue,gucci
vogue2, gucci2
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

### 使用代理 (可选)

如果不能够顺利访问和下载tumblr的内容,你应该配置一下代理.

文件格式参考`./proxies_sample1.json`和`./proxies_sample2.json`.
然后把你的代理信息用json的格式写入`./proxies.json`.
你可以访问<http://jsonlint.com/>以确保你的格式是正确的.

如果文件`./proxies.json`没有任何内容,下载过程中不会使用代理.

如果你是全局模式使用Shadowsocks做代理, 此时你的`./proxies.json`文件可以写入如下内容,

```json
{
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080"
}
```

然后重新运行下载命令.

## 喜欢就打赏吧!

如果您喜欢这个项目, 那就打个赏支持一下作者吧! 非常感谢!

<p align="center"><img src="https://raw.githubusercontent.com/dixudx/tumblr-crawler/master/alipay.png" width="250"></p>
