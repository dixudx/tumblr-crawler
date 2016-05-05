tumblr-crawlder
===============

This is a [Python](https://www.python.org) script that you can easily download
all the photos and videos from your favorite tumblr blogs.

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

* Run `pip install xmltodict requests` in your terminal ([Windows terminal](http://windows.microsoft.com/en-us/windows-vista/open-a-command-prompt-window),
[Mac OS terminal](http://www.howtogeek.com/210147/how-to-open-terminal-in-the-current-os-x-finder-location/))

* Download the [zip file](https://github.com/dixudx/tumblr-crawler/archive/master.zip) and Unzip.


## Configuration and Downloading

Find a text editor and open the file `tumblr-photo-video-ripper.py`

Most of the codes in this file can be ignored if you have no knowledge of
Python or Programming. Just move to the buttom, you will see

```python
if __name__ == "__main__":
    # tumblr subdomain, e.g. "example1" for "example1.tumblr.com"
    # you can expand the length of sites for your needs
    # sites=["single-site-example"]
    sites = ["example1", "example2", "example3"]
```

Just modify the value of `sites` by entering your favorite tumblr blogs here.

And then save the file, and run `python tumblr-photo-video-ripper.py`
in your terminal or just **double click the file** which will be automatically run by Python.

The photos/videos will be saved to the folders named with the tumblr blog.
You will find them in the current path/directory.

This script will **not re-download** the photos or videos
if they have already been downloaded. So it will **do no harm** by running this
script several times. In the meanwhile, you can find back the **missing** photos
or videos.

### More customizations for Programmers Only

```
# Setting timeout
TIMEOUT = 10

# Retry times
RETRY = 5

# Medium Index Number that Starts from
START = 0

# Numbers of photos/videos per page
MEDIA_NUM = 50
```

You can set `TIMEOUT` to another value, e.g. 50, according to
your network quality.

And this script will retry downloading the images or videos several
times (default value is 5).

You can also only download photos or videos by commenting

```python
def download_media(site):
    #download_photos(site)
    download_videos(site)
```

or

```python
def download_media(site):
    download_photos(site)
    #download_videos(site)
```


## 中文版教程请[移步这里](./README_CN.md)
