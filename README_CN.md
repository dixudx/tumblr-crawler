tumblr-crawlder
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

找到一个文字编辑器,然后打开文件`tumblr-photo-video-ripper.py`

如果不懂编程,直接忽略里面的代码,直接跳到最后一行.

```python
if __name__ == "__main__":
    # tumblr subdomain, e.g. "example1" for "example1.tumblr.com"
    # you can expand the length of sites for your needs
    # sites=["single-site-example"]
    sites = ["example1", "example2", "example3"]
```

把里面的`sites`的值改成你想要下载的那些tumblr博客的名字.

比如有一个tumblr博客的网址是<htts://example1.tumblr.com>, 那么你就把`sites`改成

```python
    sites = ["example1"]
```

如果有多个这样的tumblr博客,就把`sites`改成

```python
    sites = ["example1", "example11", "example111", "example2"]
```

然后保存文件,双击运行`tumblr-photo-video-ripper.py`或者在终端(terminal)里面
运行`python tumblr-photo-video-ripper.py`

程序运行后,会默认在当前路径下面生成一个跟tumblr博客名字相同的文件夹,
照片和视频都会放在这个文件夹下面.

运行这个脚本,不会重复下载已经下载过的图片和视频,所以不用担心重复下载的问题.同时,多次运行可以
帮你找回丢失的或者删除的图片和视频.
