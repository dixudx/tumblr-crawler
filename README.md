tumblr-crawler-apiv2
===============

New Features:
* Tumblr Crawler impl by [tumblr apiv2](https://www.tumblr.com/docs/en/api/v2),Solve the authentication issue;
* You can set `POST_TYPE`(posts/likes) to download all your liked posts;

So you can download all the photos and videos from your favorite tumblr blogs.

## 中文版教程请[移步这里](./README_CN.md)

## How to Discuss

* Feel free to join our [Slack](https://tumblr-crawler.slack.com), where you can ask questions and help answer them on Slack.
* Also you can open new issue on [Github](https://github.com/dixudx/tumblr-crawler/issues/new)

## Prerequisite

#### For Programmers and Developers

You know how to install `Python` and `pip`. Then `pip install requests xmltodict`

or

```bash
$ git clone https://github.com/dixudx/tumblr-crawler.git
$ cd tumblr-crawler
$ pip install -r requirements.txt
```

#### For non-programmers


* Installing Python: refer to [this guide](http://docs.python-guide.org/en/latest/starting/installation/)

* Installing pip: refer to [installation guide](https://pip.readthedocs.org/en/stable/installing/#install-pip)

* Run `pip install xmltodict six "requests>=2.10.0" "PySocks>=1.5.6"` in your terminal ([Windows terminal](http://windows.microsoft.com/en-us/windows-vista/open-a-command-prompt-window),
[Mac OS terminal](http://www.howtogeek.com/210147/how-to-open-terminal-in-the-current-os-x-finder-location/))

* Download the [zip file](https://github.com/dixudx/tumblr-crawler/archive/master.zip) and Unzip.


## Configuration and Downloading

There are 2 ways to specify the sites you want to download, either by creating a sites.txt file or specifying in the command line parameter.

### Use sites.txt

Find a text editor and open the file `sites.txt`, add the sites you want to download into the file, separated by comma/space/tab/CR, no `.tumblr.com` suffixes. For example, if you want to download _vogue.tumblr.com_ and _gucci.tumblr.com_, compose the file like this:

```
vogue,gucci
vogue2, gucci2
```

And then save the file, and run `python tumblr-photo-video-ripper.py`
in your terminal or just **double click the file** which will be automatically run by Python.

### Use the command line parameter (only for OS experts)

If you are familiar with command lines in Windows or Unix systems, you may run the script with a parameter to specify the sites:

```bash
python tumblr-photo-video-ripper.py site1,site2
```

The site names should be separated with comma, no space and no `.tumblr.com` suffixes needed.

### How the files get downloaded and stored

The photos/videos will be saved to the folders named with the tumblr blog.
You will find them in the current path/directory.

This script will **not re-download** the photos or videos
if they have already been downloaded. So it will **do no harm** by running this
script several times. In the meanwhile, you can find back the **missing** photos
or videos.


### Use Proxies (Optional)

You may want to use proxies when downloading. Please refer to `./proxies_sample1.json` and `./proxies_sample2.json`.
And save your own proxies to `./proxies.json` in json format.
You can validate the content by visiting <http://jsonlint.com/>.

If `./proxies.json` is an empty file, no proxies will be used during downloading.

If you are using Shadowsocks with global mode, your `./proxies.json` can be,

```json
{
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080"
}
```

And now you can enjoy your downloads.
